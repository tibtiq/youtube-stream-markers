import datetime

import pytest

from src.Timestamp import Timestamp


class Test_Timestamp:
    class Test_add:
        def test_other_is_timestamp(self):
            timestamp = Timestamp()
            adjusted_seconds = 5

            adjusted_timestamp = timestamp + adjusted_seconds
            expected_timestamp = datetime.datetime.now() + datetime.timedelta(
                seconds=adjusted_seconds
            )

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_int(self):
            timestamp = Timestamp()
            adjusted_seconds = 5

            adjusted_timestamp = timestamp + adjusted_seconds
            expected_timestamp = datetime.datetime.now() + datetime.timedelta(
                seconds=adjusted_seconds
            )

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_float(self):
            timestamp = Timestamp()
            adjusted_seconds = 5.5

            adjusted_timestamp = timestamp + adjusted_seconds
            expected_timestamp = datetime.datetime.now() + datetime.timedelta(
                seconds=adjusted_seconds
            )

            assert adjusted_timestamp.datetime == expected_timestamp

    class Test_sub:
        def test_other_is_timestamp(self):
            timestamp = Timestamp()
            adjustment_seconds = 5

            adjusted_timestamp = timestamp - adjustment_seconds
            expected_timestamp = datetime.datetime.now() - datetime.timedelta(
                seconds=adjustment_seconds
            )

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_int(self):
            timestamp = Timestamp()
            adjustment_seconds = 5

            adjusted_timestamp = timestamp - adjustment_seconds
            expected_timestamp = datetime.datetime.now() - datetime.timedelta(
                seconds=adjustment_seconds
            )

            assert adjusted_timestamp.datetime == expected_timestamp

        def test_other_is_float(self):
            timestamp = Timestamp()
            adjustment_seconds = 5.5

            adjusted_timestamp = timestamp - adjustment_seconds
            expected_timestamp = datetime.datetime.now() - datetime.timedelta(
                seconds=adjustment_seconds
            )

            assert adjusted_timestamp.datetime == expected_timestamp
