# hotkey bounded in OBS triggers this script
# this script will create/append to a file
# each line in the file will correspond to the time in the VOD when the hotkey is pressed

from typing import Union
import time
import datetime
import pathlib
import logging
# pylint: disable=import-error
import obspython as obs

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HOTKEY_ID_ARRAY = []
HOTKEY_NAMES_BY_ID = {}
SCRIPT_SETTINGS = {
    'output_folder_path': None,
    # todo combine this and stream service
    'output_type': None,
    'stream_service': None,
    'start_time': None,
    'start_timestamp': None,
    'last_timestamp': None,
}


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
        f"Output folder not set in script settings"
    )
    if output_type is None and logging.root.level != logging.INFO:
        print('No marker saved, not recording or streaming.')
        return
    elif last_timestamp == convert_timestamp_to_playback_time(current_timestamp):
        logging.info('Prevented writing duplicate timestamp')
        return
    last_timestamp = convert_timestamp_to_playback_time(current_timestamp)

    output_folder_path.mkdir(parents=True, exist_ok=True)
    filename = f'{start_time} - {output_type or "DEBUG"}'
    if stream_service is not None:
        filename += f' - {stream_service}'
    filename += f'.txt'
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


def convert_timestamp_to_playback_time(timestamp: Union[float, int]):
    """Converts a timestamp (seconds) into playback time (HOUR-MINUTE-SECONDS).

    The returned playback time has padded zeros.
    """
    assert isinstance(timestamp, (float, int)), (
        'timestamp must be a float or int type.'
    )

    return time.strftime("%H:%M:%S", time.gmtime(timestamp))


def determine_streaming_service(stream_url):
    """Uses obs service type to determine stream service.
    """

    if 'youtube' in stream_url:
        return 'youtube'
    # The check for twitch feels weak, but I found it on a twitch website
    # https://help.twitch.tv/s/twitch-ingest-recommendation?language=en_US
    elif 'live-video' in stream_url:
        return 'twitch'

    return None

# callback functions
# ------------------------------------------------------------


def hotkey_callback(button_down: bool):
    """Callback function for hotkey
    """
    global SCRIPT_SETTINGS

    if button_down:
        write_timestamp(
            SCRIPT_SETTINGS['output_folder_path'],
            SCRIPT_SETTINGS['output_type'],
            SCRIPT_SETTINGS['stream_service'],
            SCRIPT_SETTINGS['start_time'],
            SCRIPT_SETTINGS['start_timestamp'],
            SCRIPT_SETTINGS['last_timestamp'],
        )


def on_event_callback(event):
    """Callback function that handles OBS frontend events.

    List of events can be found here: https://docs.obsproject.com/reference-frontend-api
    """
    global SCRIPT_SETTINGS

    # determine if streaming or recording and started or stopped
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        SCRIPT_SETTINGS['output_type'] = 'stream'
        # https://docs.obsproject.com/reference-services?highlight=service#c.obs_service_info.get_connect_info
        stream_url = obs.obs_service_get_connect_info(
            obs.obs_frontend_get_streaming_service(),
            0,
        )
        SCRIPT_SETTINGS['stream_service'] = determine_streaming_service(
            stream_url
        )
        SCRIPT_SETTINGS['start_time'] = get_timestamp('string')
        SCRIPT_SETTINGS['start_timestamp'] = get_timestamp('float')
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        SCRIPT_SETTINGS['output_type'] = 'recording'
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        SCRIPT_SETTINGS['output_type'] = None
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        SCRIPT_SETTINGS['output_type'] = None


# ------------------------------------------------------------

# OBS library hooks
# ------------------------------------------------------------


def script_description():
    """OBS hook that setups up script description in OBS UI.
    """
    description = ''
    description += '<b>Create stream markers</b><hr>'
    description += 'Script adds the ability to set a hotkey to save a timestamp to a file. '
    description += "The file's name will correspond to the start time of the stream. "
    description += "Script will only create markers if streaming or recording.<hr>"
    description += 'Debug mode enables debug settings and prints used for development.'

    return description


def script_properties():
    """OBS hook that setups script settings in OBS UI.
    """
    props = obs.obs_properties_create()

    # output folder for vod markers
    obs.obs_properties_add_text(
        props,
        'output_folder',
        'Output folder',
        obs.OBS_TEXT_DEFAULT,
    )
    # enable script's debug mode
    obs.obs_properties_add_bool(props, "debug_enabled", "Debug mode")

    return props


def script_save(settings):
    """OBS hook called when script is being saved.
    """
    # save hotkeys in script properties
    for hotkey_id in HOTKEY_ID_ARRAY:
        # save each hotkeys data_array into script settings by the hotkeys name  !! find way to use obs_hotkey_get_name instead of tracking the name manually
        obs.obs_data_set_array(
            settings,
            HOTKEY_NAMES_BY_ID[hotkey_id],
            obs.obs_hotkey_save(hotkey_id),
        )


def script_load(settings):
    """OBS hook that runs when script first loads or reloaded.
    """
    global SCRIPT_SETTINGS

    print("--- " + __file__ + " loaded ---")

    # handle OBS frontend events
    obs.obs_frontend_add_event_callback(on_event_callback)

    # create Hotkey in global OBS Settings
    SCRIPT_SETTINGS['output_folder_path'] = pathlib.Path(
        obs.obs_data_get_string(
            settings,
            'output_folder'
        ).lower(),
    )
    # hack to pass additional arguments to callback function
    def hotkey_callback_args(button_down): return hotkey_callback(button_down)
    HOTKEY_ID_ARRAY.append(obs.obs_hotkey_register_frontend(
        "SHORTCUT 1", "Scripts - create_stream_markers.py - Push create stream marker", hotkey_callback_args))
    HOTKEY_NAMES_BY_ID[HOTKEY_ID_ARRAY[len(HOTKEY_ID_ARRAY)-1]] = "SHORTCUT 1"

    # load hotkeys from script save file
    for hotkey_id in HOTKEY_ID_ARRAY:
        # get the hotkeys data_array from the script settings (was saved under the hotkeys name)  !! find way to use obs_hotkey_get_name instead of tracking the name manually
        hotkey_data_array_from_settings = obs.obs_data_get_array(
            settings,
            HOTKEY_NAMES_BY_ID[hotkey_id],
        )
        # load the saved hotkeys data_array to the new created hotkey associated with the "hotkey_id"
        obs.obs_hotkey_load(hotkey_id, hotkey_data_array_from_settings)

        obs.obs_data_array_release(hotkey_data_array_from_settings)


def script_update(settings):
    """OBS hook thats called whenever script settings get changed in OBS
    """
    global SCRIPT_SETTINGS
    SCRIPT_SETTINGS['output_folder_path'] = pathlib.Path(
        obs.obs_data_get_string(settings, 'output_folder')
    )

    if obs.obs_data_get_bool(settings, "debug_enabled"):
        logging.root.setLevel(logging.INFO)
    else:
        logging.root.setLevel(logging.CRITICAL)
# ------------------------------------------------------------
