import logging
from dataclasses import dataclass
from src.speech_recognizer_service import SpeechRecognizerService
from queue import Queue
from openai import Client
from elevenlabs import ElevenLabs
import os
import re
import elevenlabs
import httpx
import openai
import speech_recognition as sr  # type: ignore
import time

logging.basicConfig(level=logging.DEBUG)


@dataclass
class SpeechRecognizer:
    """
    A class that handles speech recognition and facilitates interaction with users via voice commands.
    It uses speech recognition, OpenAI for processing language tasks, and ElevenLabs for speech synthesis.
    """

    speech_recognizer_service: SpeechRecognizerService

    def __post_init__(self):
        """
        Initializes necessary clients for ElevenLabs (for speech synthesis), OpenAI (for language processing),
        and the speech recognizer service. Also sets up the microphone and queue for transcription.
        """
        self.eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLAB"))
        self.openai_client = Client(api_key=os.getenv("OPENAI"))
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.transcript_queue: Queue[str] = Queue()

    def listen_to_microphone(self) -> None:
        """
        Listens to the microphone, records audio, and transcribes it into text using Google Speech Recognition.
        The transcribed text is then placed in a queue for further processing.
        """
        try:
            print("Preparing... (Ctrl + C to stop)")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("You can start talking now...")
                audio_data = self.recognizer.listen(source)

            print("Transcription...")
            transcript = self.recognizer.recognize_google(audio_data, language="pl-PL")
            self.transcript_queue.put(transcript)
            print(transcript)
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")

    def find_locker_part(self, transcript_lower: str):
        match = re.search(r'(?i)numer\s+paczki\s+(P\d{0,9})', transcript_lower) or \
                re.search(r'(?i)znajdź\s+paczkomat\s+dla\s+paczki\s+(P\d{0,9})', transcript_lower)

        if match:
            package_number = match.group(1)
            locker_info = self.speech_recognizer_service.find_locker(package_number)
            self.speak_response(locker_info)

    def generate_report_part(self, transcript_lower: str):
        if re.search(r'\bwygeneruj\s+raport\b', transcript_lower):
            report = self.speech_recognizer_service.read_report()
            self.speak_response(report)

    def end_conversation(self, transcript_lower: str) -> bool:
        if transcript_lower in ['zakończ', 'koniec', 'wyjdź']:
            print('Ending program at user request...')
            goodbye_message = 'Thank you for the conversation. See you next time!'
            print(f'AI: {goodbye_message}')
            self.speak_response(goodbye_message)
            return True
        return False

    def speak_response(self, text: str) -> None:
        """
        Converts text to speech and plays the response.
        """
        audio = self.eleven_client.generate(text=text, voice='Bill')
        elevenlabs.play(audio)

    def process_translation(self, transcript_result: str) -> None:
        """
        Processes translation requests based on the recognized speech.
        """
        transcript_lower = transcript_result.strip().lower()
        match = re.search(r'(?i)przetłumacz\s+na\s+([a-zA-Z]+)', transcript_lower)

        if match:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a professional translation assistant. "
                                "The user will speak in Polish, and your task is to translate their speech into the language they specify in their input. "
                                "The user will indicate the target language by including a phrase like 'Translate to Spanish' or 'Translate to German' at the beginning of their message. "
                                "For example, if the user says 'Przetłumacz na francuski: Jak się masz?', your response should only include the French translation 'Comment ça va?'. "
                                "Always respond only with the translated text in the target language, without any additional comments or explanations."
                            )
                        },
                        {
                            "role": "user",
                            "content": transcript_result
                        }
                    ]
                )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:
                    print("Rate limit exceeded. Retrying after 10 seconds...")
                    time.sleep(10)
                    return self.process_translation(transcript_result)
                else:
                    print(f"HTTP Error {e.response.status_code}: {e.response.text}")
                    return

            text = response.choices[0].message.content
            self.speak_response(text)

    def handle_conversation(self) -> None:
        """
        Handles the overall conversation by continuously listening to the microphone for commands.
        Processes recognized speech, performs actions such as package tracking, report generation,
        translation, and responds with synthesized speech. Terminates when the user issues a stop command.
        """
        try:
            while True:
                self.listen_to_microphone()
                transcript_result = self.transcript_queue.get()
                transcript_lower = transcript_result.strip().lower()

                self.find_locker_part(transcript_lower)
                self.generate_report_part(transcript_lower)
                self.process_translation(transcript_result)

                if self.end_conversation(transcript_lower):
                    break

        except KeyboardInterrupt:
            print("Program interrupted by the user.")
            self.speak_response('Thank you for the conversation. See you next time!')
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print("End of conversation.")
