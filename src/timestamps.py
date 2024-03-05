"""This module contains useful functions related to manipulating datetime objects."""


import datetime
import time
from typing import Union


def get_timestamp(output_format, date_format='%Y-%m-%d %H-%M-%S'):
    """Return the POSIX timestamp.

    Supported output formats are "float" and "string".
    "float" returns the timestamp as a float.
    "string" returns the timestamp in the following format: "HOUR-MINUTE-SECONDS", where zeros are
    always padded
    """
    supported_formats = ['float', 'string']
    assert output_format in supported_formats, f'Choose a supported format, {supported_formats}'

    timestamp = datetime.datetime.now()

    if output_format == 'float':
        timestamp = timestamp.timestamp()
    elif output_format == 'string':
        timestamp = timestamp.strftime(date_format)

    return timestamp


def convert_timestamp_to_playback_time(
    timestamp: Union[float, int],
    playback_format: str = "%H:%M:%S"
):
    """Convert a timestamp (seconds) into playback time (HOUR-MINUTE-SECONDS).

    The returned playback time has padded zeros.
    """
    assert isinstance(timestamp, (float, int)), (
        'timestamp must be a float or int type.'
    )

    return time.strftime(playback_format, time.gmtime(timestamp))


def convert_playback_time_to_timestamp(
    playback_time: str,
    playback_format: str = "%H:%M:%S",
):
    """Convert playback time format to timestamp format."""
    return datetime.datetime.strptime(playback_time, playback_format)
