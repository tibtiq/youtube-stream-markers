"""This module contains useful functions related to manipulating datetime objects."""

from __future__ import annotations

import datetime
import time
from typing import Optional, Union


class StreamMarker:
    """Wrapper class for datetime.datetime objects.

    This class made with the goal of working with youtube stream markers.
    """

    def __init__(
        self,
        stream_marker_time: Optional[datetime.datetime] = None,
        stream_marker_format: str = '%H:%M:%S'
    ) -> None:
        """Create a StreamMarker class with an underlying datetime.datetime object of now.

        Args:
            stream_marker_format: str, optional ['%H:%M:%S']
                Timestamp format to use when convert StreamMarker into a str. Default value uses
                padded zeros. For example:
                01:23:45
                20:03:45
            stream_marker_time: str [None]
                Used to create a StreamMarker object with a specific time.

        """
        if isinstance(stream_marker_time, datetime.datetime):
            self.datetime = stream_marker_time
        else:
            self.datetime = datetime.datetime.now()
        self.stream_marker_format = stream_marker_format

    def __str__(self) -> str:
        """Return str representation of StreamMarker."""
        return self.datetime.strftime(self.stream_marker_format)

    def __add__(self, other) -> Union[int, StreamMarker]:
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
            adjusted_timestamp = self.datetime + time_diff
            return StreamMarker(adjusted_timestamp)

        raise TypeError(
            f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'"
        )

    def __sub__(self, other) -> Union[int, StreamMarker]:
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
            adjusted_timestamp = self.datetime - time_diff
            return StreamMarker(adjusted_timestamp)
        if other is None:
            return 0

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

        return False

    def change_stream_marker_format(self, new_format: str) -> None:
        """Change StreamMarker format used when converting StreamMarker into string.

        Args:
            new_format: str
                New format to replace current stream_marker_format.
        """
        self.stream_marker_format = new_format

    def as_playback_time(self, start_time: StreamMarker) -> str:
        """Convert StreamMarker to playback time (HOUR-MINUTE-SECONDS) given a starting StreamMarker.

        The returned playback time has padded zeros.

        Args:
            playback_time: str
                StreamMarker converted to playback time given a starting StreamMarker.
        """
        if not isinstance(start_time, StreamMarker):
            raise TypeError("Value passed to 'start_time' isn't a StreamMarker object")

        return time.strftime(
            self.stream_marker_format, time.gmtime(
                (self.datetime - start_time.datetime).total_seconds()
            )
        )
