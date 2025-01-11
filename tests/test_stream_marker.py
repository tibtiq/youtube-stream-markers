import datetime

import pytest

from stream_marker import StreamMarker

# todo fixture to create a StreamMarker


class Test_StreamMarker:
    class Test_to_string:
        def test_HH_MM_SS(self):
            stream_marker = StreamMarker()
            expected_format = '%H:%M:%S'
            stream_marker_str = stream_marker.as_str(expected_format)

            assert isinstance(stream_marker_str, str)
            assert stream_marker_str == stream_marker.datetime.strftime(expected_format)

    class Test_add:
        def test_other_is_stream_marker(self):
            stream_marker = StreamMarker()
            adjustment_seconds = 5
            other_stream_marker = StreamMarker(
                datetime.datetime.now() + datetime.timedelta(
                    seconds=adjustment_seconds
                )
            )

            with pytest.raises(TypeError):
                stream_marker += other_stream_marker

        def test_other_is_none(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker + None

        def test_other_is_int(self):
            stream_marker = StreamMarker()
            adjusted_seconds = 5

            adjusted_stream_marker = stream_marker + adjusted_seconds
            expected_stream_marker = datetime.datetime.now() + datetime.timedelta(
                seconds=adjusted_seconds
            )

            assert adjusted_stream_marker.datetime == expected_stream_marker

        def test_other_is_float(self):
            stream_marker = StreamMarker()
            adjusted_seconds = 5.5

            adjusted_stream_marker = stream_marker + adjusted_seconds
            expected_stream_marker = datetime.datetime.now() + datetime.timedelta(
                seconds=adjusted_seconds
            )

            assert adjusted_stream_marker.datetime == expected_stream_marker

        def test_other_is_str(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker + 'test'

    class Test_sub:
        def test_other_is_stream_marker(self):
            stream_marker = StreamMarker()
            adjustment_seconds = 5
            other_stream_marker = StreamMarker(
                datetime.datetime.now() - datetime.timedelta(
                    seconds=adjustment_seconds
                )
            )

            time_diff_seconds = stream_marker - other_stream_marker

            assert time_diff_seconds == adjustment_seconds

        def test_other_is_none(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker - None

        def test_other_is_int(self):
            stream_marker = StreamMarker()
            adjustment_seconds = 5

            adjusted_stream_marker = stream_marker - adjustment_seconds
            expected_stream_marker = datetime.datetime.now() - datetime.timedelta(
                seconds=adjustment_seconds
            )

            assert adjusted_stream_marker.datetime == expected_stream_marker

        def test_other_is_float(self):
            stream_marker = StreamMarker()
            adjustment_seconds = 5.5

            adjusted_stream_marker = stream_marker - adjustment_seconds
            expected_stream_marker = datetime.datetime.now() - datetime.timedelta(
                seconds=adjustment_seconds
            )

            assert adjusted_stream_marker.datetime == expected_stream_marker

        def test_other_is_str(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker - 'test'

    class Test_eq:
        def test_other_is_stream_marker(self):
            now = datetime.datetime.now()
            stream_marker = StreamMarker(now)
            stream_marker2 = StreamMarker(now)

            result = stream_marker == stream_marker2

            assert result is True

        def test_other_is_datetime(self):
            now = datetime.datetime.now()
            stream_marker = StreamMarker(now)

            result = stream_marker == now

            assert result is True

        def test_other_is_none(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker - None

        def test_other_is_int(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker == 5

        def test_other_is_float(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker == 5.5

        def test_other_is_str(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker == 'test'

    class Test_le:
        def test_other_is_stream_marker(self):
            now = datetime.datetime.now()
            stream_marker = StreamMarker(now)
            stream_marker2 = StreamMarker(now)

            result = stream_marker <= stream_marker2

            assert result is True

        def test_other_is_datetime(self):
            now = datetime.datetime.now()
            stream_marker = StreamMarker(now)

            result = stream_marker <= now

            assert result is True

        def test_other_is_none(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker <= None

        def test_other_is_int(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker <= 5

        def test_other_is_float(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker <= 5.5

        def test_other_is_str(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker <= 'test'

    class Test_ge:
        def test_other_is_stream_marker(self):
            now = datetime.datetime.now()
            stream_marker = StreamMarker(now)
            stream_marker2 = StreamMarker(now)

            result = stream_marker >= stream_marker2

            assert result is True

        def test_other_is_datetime(self):
            now = datetime.datetime.now()
            stream_marker = StreamMarker(now)

            result = stream_marker >= now

            assert result is True

        def test_other_is_none(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result_stream_marker = stream_marker >= None

        def test_other_is_int(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker >= 5

        def test_other_is_float(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker >= 5.5

        def test_other_is_str(self):
            stream_marker = StreamMarker()

            with pytest.raises(TypeError):
                result = stream_marker >= 'test'

    class Test_as_playback_time:
        def test_expected_use(self):
            start_time = StreamMarker()
            end_time = start_time + 5

            playback_time = end_time.as_playback_time(start_time)

            assert playback_time == '00:00:05'

        def test_start_time_invalid_type(self):
            start_time = StreamMarker()
            end_time = start_time + 5

            with pytest.raises(TypeError):
                playback_time = end_time.as_playback_time('test')

        def test_time_format_invalid_type(self):
            start_time = StreamMarker()
            end_time = start_time + 5

            expected_assert_message = "Value passed to 'time_format' isn't a str"
            with pytest.raises(TypeError) as info:
                playback_time = end_time.as_playback_time(start_time, time_format=12)
            assert expected_assert_message in str(info.value)
