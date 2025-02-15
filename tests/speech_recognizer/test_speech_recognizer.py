import logging
import re
from asyncio import Queue
from unittest.mock import patch, MagicMock

import elevenlabs
import httpx
import pytest
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


def test_handle_conversation_find_locker(mock_speech_recognizer, mock_service):
    mock_speech_recognizer.listen_to_microphone= MagicMock(side_effect=lambda: mock_speech_recognizer.transcript_queue.put("numer Paczki P12345"))
    mock_speech_recognizer.eleven_client.generate = MagicMock(return_value="audio")
    #elevenlabs.play = MagicMock()


    mock_speech_recognizer.handle_conversation()

    mock_speech_recognizer.listen_to_microphone.assert_called_once()
    mock_service.find_locker.assert_called_once_with("p12345")
    mock_speech_recognizer.eleven_client.generate.assert_called_once()


def test_handle_conversation_read_report(mock_speech_recognizer, mock_service):
    mock_speech_recognizer.listen_to_microphone= MagicMock(side_effect=lambda: mock_speech_recognizer.transcript_queue.put("wygeneruj raport"))
    #elevenlabs.play = MagicMock()
    mock_speech_recognizer.handle_conversation()
    mock_service.read_report.assert_called_once()
    #elevenlabs.play.assert_called_once()

def test_handle_conversation_end(mock_speech_recognizer, capsys):

    mock_speech_recognizer.listen_to_microphone = MagicMock(side_effect=lambda: mock_speech_recognizer.transcript_queue.put("koniec"))
    mock_speech_recognizer.handle_conversation()
    captured = capsys.readouterr()
    assert 'Ending program at user request...' in captured.out
    assert 'AI: Thank you for the conversation. See you next time!' in captured.out


def test_handle_conversation_translation(mock_speech_recognizer, mock_service):
    mock_speech_recognizer.transcript_queue.put("przetłumacz na angielski")


    mock_speech_recognizer.openai_client.chat.completions.create = MagicMock(
        return_value=MagicMock(choices=[MagicMock(message=MagicMock(content="Translate to English"))])
    )

    with patch.object(mock_speech_recognizer, "handle_conversation", side_effect=StopIteration):
        with pytest.raises(StopIteration):
            next(mock_speech_recognizer.handle_conversation())

    mock_speech_recognizer.openai_client.chat.completions.create.assert_called_once()


# def test_handle_conversation_http_429(mock_speech_recognizer, mock_service):
#     # Symulujemy odpowiedź z błędem 429 (Rate Limit)
#     mock_error_response = MagicMock()
#     mock_error_response.status_code = 429
#     mock_error = httpx.HTTPStatusError("Rate limit exceeded", request=None, response=mock_error_response)
#
#     # OpenAI zawsze zgłasza ten błąd
#     mock_speech_recognizer.openai_client.chat.completions.create = MagicMock(side_effect=mock_error)
#
#     # Symulujemy wprowadzenie komendy tłumaczenia
#     mock_speech_recognizer.listen_to_microphone = MagicMock(
#         side_effect=lambda: mock_speech_recognizer.transcript_queue.put("przetłumacz na angielski")
#     )
#
#     with patch("time.sleep", return_value=None) as mock_sleep:
#         mock_speech_recognizer.handle_conversation()
#
#     # Sprawdzamy, czy kod próbował ponownie po błędzie 429
#     mock_sleep.assert_called_with(10)
#     mock_speech_recognizer.openai_client.chat.completions.create.assert_called()


