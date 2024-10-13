import pytest

from src.youtube_interface import (
    get_youtube_credentials_from_file,
    get_youtube_credentials_from_oauth,
)


class Test_get_youtube_credentials_from_file:
    class Test_asserts:
        def test_path_doesnt_exist(self, tmp_path):
            path = tmp_path / 'file.json'
            expected_assert_message = "The provided path for api credentials doesn't exist"

            with pytest.raises(AssertionError) as info:
                get_youtube_credentials_from_file(path)
            assert expected_assert_message in str(info.value)

        def test_path_file_type_incorrect(self, tmp_path):
            path = tmp_path / 'file.txt'
            open(path, 'w', encoding='utf-8')
            expected_assert_message = (
                'The provided path for api credentials appears to be incorrect file type. '
                'Expected file type is "dat"'
            )

            with pytest.raises(AssertionError) as info:
                get_youtube_credentials_from_file(path)
            assert expected_assert_message in str(info.value)


class Test_get_youtube_credentials_from_oauth:
    class Test_asserts:
        def test_path_doesnt_exist(self, tmp_path):
            path = tmp_path / 'file.json'
            expected_assert_message = "The provided path for api credentials doesn't exist"

            with pytest.raises(AssertionError) as info:
                get_youtube_credentials_from_oauth(path)
            assert expected_assert_message in str(info.value)

        def test_path_file_type_incorrect(self, tmp_path):
            path = tmp_path / 'file.txt'
            open(path, 'w', encoding='utf-8')
            expected_assert_message = (
                "The provided path for api credentials appears to be incorrect file type."
            )

            with pytest.raises(AssertionError) as info:
                get_youtube_credentials_from_oauth(path)
            assert expected_assert_message in str(info.value)
