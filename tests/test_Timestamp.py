import datetime

import pytest

from src.timestamp import Timestamp

# todo fixture to create a timestamp


class Test_Timestamp:
    class Test_str:
        def test_str(self):
            timestamp = Timestamp()

            assert isinstance(str(timestamp), str)
            assert str(timestamp) == timestamp.datetime.strftime(timestamp.timestamp_format)

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

    class Test_eq:
        def test_other_is_timestamp(self):
            now = datetime.datetime.now()
            timestamp = Timestamp(now)
            timestamp2 = Timestamp(now)

            result = timestamp == timestamp2

            assert result is True

        def test_other_is_datetime(self):
            now = datetime.datetime.now()
            timestamp = Timestamp(now)

            result = timestamp == now

            assert result is True

        def test_other_is_none(self):
            timestamp = Timestamp()

            result = timestamp is None

            assert result is False

        def test_other_is_int(self):
            timestamp = Timestamp()

            result = timestamp == 5

            assert result is False

        def test_other_is_float(self):
            timestamp = Timestamp()

            result = timestamp == 5.5

            assert result is False

        def test_other_is_str(self):
            timestamp = Timestamp()

            result = timestamp == 'test'

            assert result is False

    class Test_change_timestamp_format:
        def test_timestamp_format_changes(self):
            timestamp = Timestamp()
            new_format = '%d/%m/%y %H:%M:%S.%f'

            timestamp.change_timestamp_format(new_format)

            assert timestamp.timestamp_format == new_format

    class Test_as_playback_time:
        def test_expected_use(self):
            start_time = Timestamp()
            end_time = start_time + 5

            playback_time = end_time.as_playback_time(start_time)

            assert playback_time == '00:00:05'

        def test_invalid_type(self):
            start_time = Timestamp()
            end_time = start_time + 5

            with pytest.raises(TypeError):
                playback_time = end_time.as_playback_time('test')
