from unittest.mock import MagicMock

import pytest

from src.speech_recognizer import SpeechRecognizer
from src.speech_recognizer_service import SpeechRecognizerService


@pytest.fixture
def mock_speech_recognizer_service():
    """
    Fixture to create a mocked instance of the `SpeechRecognizerService` class.

    This fixture mocks the `find_locker` and `read_report` methods to return predefined responses.
    It is used to simulate the behavior of the `SpeechRecognizerService` without needing to
    interact with actual data or external services.

    Returns:
        MagicMock: A mocked `SpeechRecognizerService` object with predefined return values.
    """
    mock_service = MagicMock()
    mock_service.find_locker.return_value = "Your package P123 is in locker 5"
    mock_service.read_report.return_value = "Sample report content"
    return mock_service


@pytest.fixture
def mock_eleven_client():
    """
    Fixture to create a mocked instance of the Eleven Labs client.

    This fixture mocks the `generate` method to simulate the audio generation process without
    needing to interact with the actual Eleven Labs service.

    Returns:
        MagicMock: A mocked Eleven Labs client with predefined return values.
    """
    eleven_client = MagicMock()
    eleven_client.generate.return_value = "audio"
    return eleven_client


@pytest.fixture
def mock_openai_client():
    """
    Fixture to create a mocked instance of the OpenAI client.

    This fixture mocks the `chat.completions.create` method to simulate the behavior of OpenAI's
    chat completion without needing to make actual requests to OpenAI. It returns a predefined
    translated message.

    Returns:
        MagicMock: A mocked OpenAI client that simulates chat completions.
    """
    openai_client = MagicMock()
    openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Translated text"))]
    )
    return openai_client


@pytest.fixture
def speech_recognizer(mock_speech_recognizer_service):
    """
    Fixture to create an instance of the `SpeechRecognizer` class.

    This fixture initializes a `SpeechRecognizer` object using the mocked `SpeechRecognizerService`.
    The mock allows the `SpeechRecognizer` class to interact with predefined responses rather than
    requiring real service calls.

    Args:
        mock_speech_recognizer_service (MagicMock): A mocked version of the `SpeechRecognizerService`.

    Returns:
        SpeechRecognizer: An instance of `SpeechRecognizer` initialized with the mocked service.
    """
    return SpeechRecognizer(mock_speech_recognizer_service)


@pytest.fixture
def mock_service():
    mock_service = MagicMock(spec=SpeechRecognizerService)
    return mock_service

@pytest.fixture
def mock_speech_recognizer(mock_service: MagicMock):
    return SpeechRecognizer(mock_service)