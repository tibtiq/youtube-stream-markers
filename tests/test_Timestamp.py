import datetime

import pytest

from src.Timestamp import Timestamp


class Test_Timestamp:
    class Test_add:
        def test_other_is_timestamp(self):
            timestamp = Timestamp()
            adjusted_timestamp = timestamp + 5

            expected_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=5)

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_int(self):
            timestamp = Timestamp()
            adjusted_timestamp = timestamp + 5

            expected_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=5)

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_float(self):
            timestamp = Timestamp()
            adjusted_timestamp = timestamp + 5.5

            expected_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=5.5)

            assert adjusted_timestamp.datetime == expected_timestamp

    class Test_sub:
        def test_other_is_timestamp(self):
            timestamp = Timestamp()
            adjusted_timestamp = timestamp - 5

            expected_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=5)

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_int(self):
            timestamp = Timestamp()
            adjusted_timestamp = timestamp - 5

            expected_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=5)

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_float(self):
            timestamp = Timestamp()
            adjusted_timestamp = timestamp - 5.5

            expected_timestamp = datetime.datetime.now() - datetime.timedelta(seconds=5.5)

            assert adjusted_timestamp.datetime == expected_timestamp
