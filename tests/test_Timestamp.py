import datetime

import pytest

from src.Timestamp import Timestamp


class Test_Timestamp:
    class Test_str:
        def test_str_representation(self):
            timestamp = Timestamp()

            assert timestamp.datetime.strftime(timestamp.timestamp_format) == str(timestamp)

    class Test_add:
        def test_other_is_timestamp(self):
            timestamp = Timestamp()
            adjustment_seconds = 5
            other_timestamp = Timestamp(
                datetime.datetime.now() + datetime.timedelta(
                    seconds=adjustment_seconds
                )
            )

            with pytest.raises(TypeError):
                timestamp += other_timestamp

        def test_other_is_none(self):
            timestamp = Timestamp()

            with pytest.raises(TypeError):
                result_timestamp = timestamp + None

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

        def test_other_is_str(self):
            timestamp = Timestamp()

            with pytest.raises(TypeError):
                result_timestamp = timestamp + 'test'

    class Test_sub:
        def test_other_is_timestamp(self):
            timestamp = Timestamp()
            adjustment_seconds = 5
            other_timestamp = Timestamp(
                datetime.datetime.now() - datetime.timedelta(
                    seconds=adjustment_seconds
                )
            )

            time_diff_seconds = timestamp - other_timestamp

            assert time_diff_seconds == adjustment_seconds

        def test_other_is_none(self):
            timestamp = Timestamp()

            result_timestamp = timestamp - None

            assert result_timestamp == 0

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

        def test_other_is_str(self):
            timestamp = Timestamp()

            with pytest.raises(TypeError):
                result_timestamp = timestamp - 'test'
