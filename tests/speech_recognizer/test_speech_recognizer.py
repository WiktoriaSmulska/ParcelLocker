from src.speech_recognizer import SpeechRecognizer
from src.speech_recognizer_service import SpeechRecognizerService
from unittest.mock import patch, MagicMock
import logging
import time
import elevenlabs
import httpx
import pytest
import speech_recognition as sr


logging.basicConfig(level=logging.DEBUG)

@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", return_value="numer paczki P123")
def test_listen_to_microphone(mock_listen, mock_recognize, speech_recognizer):
    """
        Tests if the microphone listening function correctly places transcribed speech into the queue.
    """
    speech_recognizer.listen_to_microphone()

    assert not speech_recognizer.transcript_queue.empty()
    assert speech_recognizer.transcript_queue.get() == "numer paczki P123"


@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", side_effect=sr.UnknownValueError)
def test_listen_to_microphone_unknown_value1(mock_listen, mock_recognize, speech_recognizer, capsys):
    """
    Tests if the microphone listening function correctly handles cases where speech cannot be recognized.
    """
    speech_recognizer.listen_to_microphone()

    assert speech_recognizer.transcript_queue.empty()

    captured = capsys.readouterr()
    assert "Could not understand the audio." in captured.out

@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", side_effect=sr.RequestError)
def test_listen_to_microphone_unknown_value2(mock_listen, mock_recognize, speech_recognizer, capsys):
    """
    Tests if the microphone listening function correctly handles cases where the speech recognition service fails.
    """
    speech_recognizer.listen_to_microphone()

    assert speech_recognizer.transcript_queue.empty()

    result = capsys.readouterr()
    assert "Preparing..." in result.out
    assert "Could not request results from Google Speech Recognition service." in result.out


def test_handle_conversation_find_locker(mock_speech_recognizer, mock_service):
    """
    Tests if the system correctly identifies and retrieves locker information based on a spoken package number.
    """
    mock_speech_recognizer.speak_response = MagicMock()
    mock_service.find_locker.return_value = "Your package p12345 is in locker L003"
    transcript = "numer paczki p12345"

    mock_speech_recognizer.find_locker_part(transcript)

    mock_service.find_locker.assert_called_once_with("p12345")
    mock_speech_recognizer.speak_response.assert_called_once_with("Your package p12345 is in locker L003")

def test_handle_conversation_generate_report(mock_speech_recognizer, mock_service):
    """
    Tests if the system correctly retrieves and speaks out a report when requested.
    """
    mock_speech_recognizer.speak_response = MagicMock()
    mock_service.read_report.return_value = "Report data"

    mock_speech_recognizer.generate_report_part("wygeneruj raport")

    mock_service.read_report.assert_called_once()
    mock_speech_recognizer.speak_response.assert_called_once_with("Report data")

def test_handle_conversation_end_true(mock_speech_recognizer, mock_service):
    """
    Tests if the conversation correctly ends when the user gives a termination command.
    """
    mock_speech_recognizer.speak_response = MagicMock()


    mock_speech_recognizer.end_conversation("koniec")
    mock_speech_recognizer.speak_response.assert_called_once_with("Thank you for the conversation. See you next time!")


def test_handle_conversation_end_false(mock_speech_recognizer, mock_service):
    """
    Tests if the conversation continues when the user gives an unrecognized command.
    """
    mock_speech_recognizer.speak_response = MagicMock()


    mock_speech_recognizer.end_conversation("costam")
    mock_speech_recognizer.speak_response.assert_not_called()

def test_handle_conversation_speak(mock_speech_recognizer, mock_service):
    """
    Tests if the text-to-speech function correctly generates and plays audio.
    """
    mock_speech_recognizer.eleven_client.generate = MagicMock()
    elevenlabs.play = MagicMock()

    mock_speech_recognizer.speak_response("text")
    mock_speech_recognizer.eleven_client.generate.assert_called_once_with(text="text", voice='Bill')
    elevenlabs.play.assert_called_once()


def test_process_translation(mock_speech_recognizer, mock_service):
    """
    Tests if the system correctly translates a given input and speaks the translated text.
    """
    mock_speech_recognizer.openai_client = MagicMock()
    mock_speech_recognizer.speak_response = MagicMock()

    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = "hello, how are you?"
    mock_response.choices = [mock_choice]
    mock_speech_recognizer.openai_client.chat.completions.create.return_value = mock_response

    transcript = "przetłumacz na angielski: hej jak się masz?"
    mock_speech_recognizer.process_translation(transcript)

    mock_speech_recognizer.openai_client.chat.completions.create.assert_called_once()

    mock_speech_recognizer.speak_response.assert_called_once_with("hello, how are you?")


# def test_process_translation_rate_limit(mock_speech_recognizer):
#     time.sleep = MagicMock()
#     mock_speech_recognizer.openai_client = MagicMock()
#     mock_speech_recognizer.speak_response = MagicMock()
#
#     mock_request = MagicMock()
#
#     mock_speech_recognizer.openai_client.chat.completions.create.side_effect =\
#         httpx.HTTPStatusError(
#             "429 Too Many Requests", request=mock_request, response=MagicMock(status_code=429)
#         )
#
#     transcript = "Przetłumacz na angielski: Jak się masz?"
#     mock_speech_recognizer.process_translation(transcript)
#
#     time.sleep.assert_called_once_with(10)

def test_handle_conversation(mock_speech_recognizer, mock_service):
    """
    Tests if the conversation handling function processes a full cycle of recognition and response.
    """
    mock_speech_recognizer.listen_to_microphone = MagicMock(
        side_effect=lambda: mock_speech_recognizer.transcript_queue.put("wygeneruj raport")
    )

    mock_speech_recognizer.generate_report_part = MagicMock()
    mock_speech_recognizer.find_locker_part = MagicMock()
    mock_speech_recognizer.process_translation = MagicMock()
    mock_speech_recognizer.end_conversation = MagicMock(return_value=True)  # Kończy pętlę po pierwszym obiegu

    mock_speech_recognizer.handle_conversation()

    mock_speech_recognizer.generate_report_part.assert_called_once_with("wygeneruj raport")


def test_handle_conversation_exceptions(mock_speech_recognizer):
    """
    Tests if the system correctly handles exceptions, including keyboard interruptions and unexpected errors.
    """
    mock_speech_recognizer.listen_to_microphone = MagicMock(side_effect=KeyboardInterrupt)
    mock_speech_recognizer.speak_response = MagicMock()

    try:
        mock_speech_recognizer.handle_conversation()
    except KeyboardInterrupt:
        pass

    mock_speech_recognizer.speak_response.assert_called_once_with('Thank you for the conversation. See you next time!')

    mock_speech_recognizer.listen_to_microphone = MagicMock(side_effect=Exception("Unexpected error"))

    try:
        mock_speech_recognizer.handle_conversation()
    except Exception as e:
        assert str(e) == "Unexpected error"