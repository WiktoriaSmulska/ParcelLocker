import logging
from unittest.mock import patch, MagicMock
import speech_recognition as sr
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

#TODO czemu na tym teście poniżej program się zawiesza?
#TODO czy dobrze w tym teście wszystko mockuje czy może powinnam to jakoś inaczej zrobić?
@patch("speech_recognition.Recognizer.listen")
@patch("speech_recognition.Recognizer.recognize_google", return_value="numer paczki P123")
def test_handle_conversation_package(mock_listen, mock_recognize, speech_recognizer, capsys):
    speech_recognizer.listen_to_microphone = MagicMock(return_value=None)

    speech_recognizer.transcript_queue.get = MagicMock(return_value="numer paczki p123")

    speech_recognizer.eleven_client.generate = MagicMock(return_value=b"Generated audio")

    speech_recognizer.eleven_client.play = MagicMock()

    speech_recognizer.speech_recognizer_service.find_locker = MagicMock(return_value="Your package P123 is in locker 5")

    with patch("builtins.input", side_effect=["numer paczki p123", "zakończ"]):
        speech_recognizer.handle_conversation()

    speech_recognizer.speech_recognizer_service.find_locker.assert_called_once_with("p123")

    speech_recognizer.eleven_client.generate.assert_called_once_with(
        text="Your package P123 is in locker 5", voice='Bill'
    )

    #speech_recognizer.eleven_client.play.assert_called_once()
    generated_audio = speech_recognizer.eleven_client.generate.return_value
    #logging.debug(f"Generated audio type: {type(generated_audio)}")  # Should be <class 'bytes'>

    captured = capsys.readouterr()
    assert "Your package P123 is in locker 5" in captured.out
