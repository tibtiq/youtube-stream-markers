"""This module contains useful functions related to manipulating datetime objects."""

from __future__ import annotations

import datetime
import time
from typing import Union


class Timestamp:
    """Wrapper class for datetime.datetime objects with the goal of working with youtube timestamps.
    """

    def __init__(self, timestamp_time: datetime.datetime = None, timestamp_format: str = '%H:%M:%S') -> None:
        """Creates a Timestamp class with an underlying datetime.datetime object of now.

        Args:
            timestamp_format: str, optional ['%H:%M:%S']
                Timestamp format to use when convert Timestamp into a str. Default value uses
                padded zeros. For example:
                01:23:45
                20:03:45
            timestamp_time: str [None]
                Used to create a Timestamp object with a specific time.

        """
        if isinstance(timestamp_time, datetime.datetime):
            self.datetime = timestamp_time
        else:
            self.datetime = datetime.datetime.now()
        self.timestamp_format = timestamp_format

    def __str__(self) -> str:
        """Returns str representation of timestamp."""
        return self.datetime.strftime(self.timestamp_format)

    def __add__(self, other) -> Union[int, Timestamp]:
        """Overloads the '+' operator for addition.

        Args:
            other: Timestamp
                The object added to this instance.

        Returns:
            An int representing the combined total seconds of other and this instance.
            A new Timestamp object with the result of the addition.
        """
        if isinstance(other, (int, float)):
            time_diff = datetime.timedelta(seconds=other)
            adjusted_timestamp = self.datetime + time_diff
            return Timestamp(adjusted_timestamp)

        raise TypeError(
            f"unsupported operand type(s) for +: '{type(self)}' and '{type(other)}'"
        )

    def __sub__(self, other) -> Union[int, Timestamp]:
        """Overloads the '-' operator for subtraction.

        Args:
            other: Timestamp
                The object subtract from this instance.

        Returns:
            An int representing the total seconds difference between other and this instance.
            A new Timestamp object with the result of the subtract.
        """
        if isinstance(other, Timestamp):
            return round((self.datetime - other.datetime).total_seconds())
        if isinstance(other, (int, float)):
            time_diff = datetime.timedelta(seconds=other)
            adjusted_timestamp = self.datetime - time_diff
            return Timestamp(adjusted_timestamp)
        if other is None:
            return 0

        raise TypeError(
            f"unsupported operand type(s) for -: '{type(self)}' and '{type(other)}'"
        )

    def __eq__(self, other: object) -> bool:
        """Overloads the '==' operator for equality comparison.

        Args:
            other: Timestamp or compatible object
                The object to compare for equality with this instance.

        Returns:
            bool: True if the objects are considered equal, False otherwise.
        """

        if isinstance(other, Timestamp):
            return self.datetime == other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime == other

        return False

    def change_timestamp_format(self, new_format: str) -> None:
        """Changes timestamp format used when converting Timestamp into string.

        Args:
            new_format: str
                New format to replace current timestamp_format.
        """
        self.timestamp_format = new_format

    def as_playback_time(self, start_time: Timestamp) -> str:
        """Converts Timestamp to playback time (HOUR-MINUTE-SECONDS) given a starting Timestamp.

        The returned playback time has padded zeros.

        Args:
            playback_time: str
                Timestamp converted to playback time given a starting Timestamp.
        """
        if not isinstance(start_time, Timestamp):
            raise TypeError("Value passed to 'start_time' isn't a Timestamp object")

        return time.strftime(
            self.timestamp_format, time.gmtime(
                (self.datetime - start_time.datetime).total_seconds()
            )
        )
