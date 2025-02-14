import logging
import re
from asyncio import Queue
from unittest.mock import patch, MagicMock
import speech_recognition as sr

from src.speech_recognizer import SpeechRecognizer
from src.speech_recognizer_service import SpeechRecognizerService

logging.basicConfig(level=logging.DEBUG)

@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", return_value="numer paczki P123")
def test_listen_to_microphone(mock_listen, mock_recognize, speech_recognizer):
    speech_recognizer.listen_to_microphone()

    assert not speech_recognizer.transcript_queue.empty()
    assert speech_recognizer.transcript_queue.get() == "numer paczki P123"


@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", side_effect=sr.UnknownValueError)
def test_listen_to_microphone_unknown_value1(mock_listen, mock_recognize, speech_recognizer, capsys):
    speech_recognizer.listen_to_microphone()

    assert speech_recognizer.transcript_queue.empty()

    captured = capsys.readouterr()
    assert "Could not understand the audio." in captured.out

@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", side_effect=sr.RequestError)
def test_listen_to_microphone_unknown_value2(mock_listen, mock_recognize, speech_recognizer, capsys):
    speech_recognizer.listen_to_microphone()

    assert speech_recognizer.transcript_queue.empty()

    result = capsys.readouterr()
    assert "Preparing..." in result.out
    assert "Could not request results from Google Speech Recognition service." in result.out



def test_handle_conversation():
    mock_service = MagicMock(spec=SpeechRecognizerService)
    speech_recognizer = SpeechRecognizer(mock_service)
    listen_mic = speech_recognizer.listen_to_microphone= MagicMock()

    speech_recognizer.transcript_queue = Queue()
    speech_recognizer.transcript_queue.put("numer Paczki P12345")
    #speech_recognizer.transcript_queue.put("koniec")

    #with patch("builtins.input", side_effect=["koniec"]):
    speech_recognizer.handle_conversation()
    transcript_result = speech_recognizer.transcript_queue.get()
    transcript_lower = transcript_result.strip().lower()

    regex_result = test_regex(transcript_lower)
    assert regex_result == "P12345"
    listen_mic.assert_called_once()

def test_regex(text:str)->str | None:
    match = re.search(r'(?i)numer\s+paczki\s+(P\d{0,9})', text) or \
            re.search(r'(?i)znajdź\s+paczkomat\s+dla\s+paczki\s+(P\d{0,9})', text)

    return match


