from unittest.mock import patch, mock_open

from src.speech_recognizer_service import SpeechRecognizerService


def test_find_locker(mock_deliver_repo) -> None:
    """
    Test the `find_locker` method of the `SpeechRecognizerService` class.

    This test verifies that the `find_locker` method correctly identifies whether
    a package exists and provides the correct locker information.

    Args:
        mock_deliver_repo (MagicMock): A mocked repository that returns predefined delivery data.

    Asserts:
        - The method returns the correct locker location for a valid package.
        - The method returns a 'does not exist' message for an invalid package.
    """
    service = SpeechRecognizerService(mock_deliver_repo)

    result1 = service.find_locker("P12345")
    assert result1 == "Your package P12345 is in locker 12345"

    result2 = service.find_locker("123")
    assert result2 == "Your package does not exist"


def test_read_report(mock_deliver_repo) -> None:
    """
    Test the `read_report` method of the `SpeechRecognizerService` class.

    This test verifies that the `read_report` method correctly reads data from a report file
    and returns the expected content. It mocks the `open` function to simulate file reading.

    Args:
        mock_deliver_repo (MagicMock): A mocked repository that returns predefined delivery data.

    Asserts:
        - The method correctly reads the file and returns the expected data.
        - The method calls the `open` function with the correct file path.
    """
    service = SpeechRecognizerService(mock_deliver_repo)
    mock_data = "test"

    with patch("builtins.open", mock_open(read_data=mock_data)) as mock_file:
        result = service.read_report()

    assert result == mock_data

    mock_file.assert_called_once_with(
        r"C:\Users\User\Desktop\proj\projects_python\projectt\data\report.txt", "r"
    )
