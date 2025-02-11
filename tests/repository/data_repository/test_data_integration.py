from pathlib import Path
from src.validator import UserDataDictValidator
from src.converter import UserConverter
from src.file_service import UserJsonFileReader
from src.model import Users
from src.repository import UserDataRepository
from src.model import UserDataDict
import json
import logging

logging.basicConfig(level=logging.DEBUG)

def test_user_data_repository_with_real_json_file(
        user_1: Users,
        user_2: Users,
        tmp_path: Path,
        user_1_data: UserDataDict,
        user_2_data: UserDataDict
) -> None:
    """
    Tests the UserDataRepository by using a real JSON file stored in a temporary directory.

    This function performs the following steps:
    1. Creates a temporary JSON file in the provided `tmp_path`.
    2. Writes sample user data (`user_1_data` and `user_2_data`) to the file.
    3. Reads the data back using the `UserDataRepository`.
    4. Verifies that the retrieved data matches the expected user objects.

    Args:
        user_1 (Users): First user instance.
        user_2 (Users): Second user instance.
        tmp_path (Path): Temporary directory for storing the JSON file.
        user_1_data (UserDataDict): Dictionary representation of `user_1`.
        user_2_data (UserDataDict): Dictionary representation of `user_2`.

    Raises:
        AssertionError: If the retrieved data does not match the expected users.
    """

    filename = "test_user.json"
    test_file = tmp_path / filename

    sample_data = [user_1_data, user_2_data]

    with open(test_file, "w") as file:

        json.dump(sample_data, file)

    user_json_file_reader = UserJsonFileReader()
    validator = UserDataDictValidator()
    converter = UserConverter()

    user_data_repository = UserDataRepository(
        file_reader=user_json_file_reader,
        validator=validator,
        converter=converter,
        filename=str(test_file)
    )

    data = user_data_repository.get_data()

    assert len(data) == 2, "Expected two users in the repository"
    assert data[0] == user_1, "First user data does not match expected user_1"
    assert data[1] == user_2, "Second user data does not match expected user_2"
