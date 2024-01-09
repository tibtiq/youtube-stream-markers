import datetime
import logging
import pathlib
import time
from typing import Union


def write_timestamp(
    output_folder_path: pathlib.Path,
    output_type: str,
    stream_service: str,
    start_time: str,
    start_timestamp: float,
    last_timestamp: str
):
    """Writes given timestamp to appropriate VOD marker textfile in given output_folder_path.

    Duplicate timestamps, ie if create stream marker is spammed, will not be created.
    The stream marker file will have the timestamp of the start of a stream/recording and the
    service being streamed on.
    """
    current_timestamp = get_timestamp('float')
    assert output_folder_path != pathlib.Path('.'), (
        'Output folder not set in script settings'
    )
    if output_type is None and logging.root.level != logging.INFO:
        print('No marker saved, not recording or streaming.')
        return
    if last_timestamp == convert_timestamp_to_playback_time(current_timestamp):
        logging.info('Prevented writing duplicate timestamp')
        return
    last_timestamp = convert_timestamp_to_playback_time(current_timestamp)

    output_folder_path.mkdir(parents=True, exist_ok=True)
    filename = f'{start_time} - {output_type or "DEBUG"}'
    if stream_service is not None:
        filename += f' - {stream_service}'
    filename += '.txt'
    output_file_path = output_folder_path / filename

    logging.info(output_file_path)
    vod_timestamp_diff = current_timestamp - start_timestamp
    with output_file_path.open('a', encoding='utf-8') as file:
        logging.info(f'Adding marker to: {output_file_path}')
        file.write(
            f'{convert_timestamp_to_playback_time(vod_timestamp_diff)}\n'
        )


def get_timestamp(output_format, date_format='%Y-%m-%d %H-%M-%S'):
    """Returns the POSIX timestamp.

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
    """Converts a timestamp (seconds) into playback time (HOUR-MINUTE-SECONDS).

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
    return datetime.datetime.strptime(playback_time, playback_format)
