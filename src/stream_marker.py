"""This module contains a class StreamMarker that is a wrapper of datetime.datetime objects.

The wrapper contains useful functions related to manipulating 00:00:00 timestamps.
"""

from __future__ import annotations

import datetime
import time


class StreamMarker:
    """Wrapper class for datetime.datetime objects.

    This class made with the goal of working with youtube stream markers.
    """

    def __init__(
        self,
        stream_marker_time: datetime.datetime | None = None,
    ) -> None:
        """Create a StreamMarker class with an underlying datetime.datetime object of now.

        Args:
            stream_marker_time: Optional[datetime.datetime] = None
                Used to create a StreamMarker object with a specific time.
        """
        if isinstance(stream_marker_time, datetime.datetime):
            self.datetime = stream_marker_time
        else:
            self.datetime = datetime.datetime.now()

    def __add__(self, other) -> int | StreamMarker:
        """Overloads the '+' operator for addition.

        Args:
            other: StreamMarker
                The object added to this instance.

        Returns:
            An int representing the combined total seconds of other and this instance.
            A new StreamMarker object with the result of the addition.
        """
        if isinstance(other, (int, float)):
            time_diff = datetime.timedelta(seconds=other)
            adjusted_time = self.datetime + time_diff
            return StreamMarker(adjusted_time)

        raise TypeError(
            f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'"
        )

    def __sub__(self, other) -> int | StreamMarker:
        """Overloads the '-' operator for subtraction.

        Args:
            other: StreamMarker
                The object subtract from this instance.

        Returns:
            An int representing the total seconds difference between other and this instance.
            A new StreamMarker object with the result of the subtract.
        """
        if isinstance(other, StreamMarker):
            return round((self.datetime - other.datetime).total_seconds())
        if isinstance(other, (int, float)):
            time_diff = datetime.timedelta(seconds=other)
            adjusted_time = self.datetime - time_diff
            return StreamMarker(adjusted_time)

        raise TypeError(
            f"unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'"
        )

    def __eq__(self, other: object) -> bool:
        """Overloads the '==' operator for equality comparison.

        Args:
            other: StreamMarker or compatible object
                The object to compare for equality with this instance.

        Returns:
            bool: True if the objects are considered equal, False otherwise.
        """
        if isinstance(other, StreamMarker):
            return self.datetime == other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime == other

        raise TypeError(
            f"unsupported operand type(s) for >=: '{type(self)}' and '{type(other)}'"
        )

    def __le__(self, other: object) -> bool:
        """Overloads the '<=' operator for less than or equal to comparison.

        Args:
            other: StreamMarker or compatible object
                The object to compare for less than or equal with this instance.

        Returns:
            bool: True if the self is less than or equal to other, False otherwise.
        """
        if isinstance(other, StreamMarker):
            return self.datetime <= other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime <= other

        raise TypeError(
            f"unsupported operand type(s) for <=: '{type(self)}' and '{type(other)}'"
        )

    def __ge__(self, other: object) -> bool:
        """Overloads the '>=' operator for greater than or equal to comparison.

        Args:
            other: StreamMarker or compatible object
                The object to compare for greater than or equal with this instance.

        Returns:
            bool: True if the self is greater than or equal to other, False otherwise.
        """
        if isinstance(other, StreamMarker):
            return self.datetime >= other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime >= other

        raise TypeError(
            f"unsupported operand type(s) for >=: '{type(self)}' and '{type(other)}'"
        )

    def __str__(self) -> str:
        """Overloads the 'str' operator for user-friendly, human-readable string representation.

        Returns:
            Str: human-readable string representation.
        """
        return f"{self.datetime}"

    def as_str(self, str_format: str = "%H:%M:%S"):
        """Return str representation of StreamMarker."""
        return self.datetime.strftime(str_format)

    def as_playback_time(
        self, start_time: StreamMarker, time_format: str = "%H:%M:%S"
    ) -> str:
        """Convert StreamMarker to playback time (HOUR-MINUTE-SECONDS) given a start stream marker.

        The returned playback time will have padded zeros.

        Example:
            stream_marker = StreamMarker(2025-01-11 17:00:10.000000)
            stream_marker.as_playback_time(stream_marker + 10)
            will return
            00:00:10

        Args:
            playback_time: str
                StreamMarker converted to playback time given a starting StreamMarker.
            stream_marker_format: str = '%H:%M:%S'
                Timestamp format to use when convert StreamMarker into a str. Default value uses
                padded zeros. For example:
                01:23:45
                20:03:45
        """
        if not isinstance(start_time, StreamMarker):
            raise TypeError("Value passed to 'start_time' isn't a StreamMarker object")
        if not isinstance(time_format, str):
            raise TypeError("Value passed to 'time_format' isn't a str")

        time_epoch_diff_secs = (self.datetime - start_time.datetime).total_seconds()
        time_utc_diff_secs = time.gmtime(time_epoch_diff_secs)
        time_formatted = time.strftime(time_format, time_utc_diff_secs)

        return time_formatted
