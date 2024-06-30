import pytest

from src.youtube_interface import get_youtube_credentials_from_oauth


class Test_get_youtube_credentials_from_oauth:
    class Test_asserts:
        def test_path_doesnt_exist(self, tmp_path):
            path = tmp_path / 'file.json'

            with pytest.raises(Exception):
                get_youtube_credentials_from_oauth(path)

        def test_path_file_type_incorrect(self, tmp_path):
            path = tmp_path / 'file.txt'
            open(path, 'w', encoding='utf-8')

            with pytest.raises(Exception):
                get_youtube_credentials_from_oauth(path)
