"""This module is an OBS script that creates stream markers for a youtube livestream.

The stream markers are placed in the description of the livestream.

"""


# todo work with datetime objects not strs

# hotkey bounded in OBS triggers this script
# this script will create/append to a file
# each line in the file will correspond to the time in the VOD when the hotkey is pressed

import logging
import pathlib

# pylint: disable-next=import-error
import obspython as obs

from timestamps import (convert_playback_time_to_timestamp,
                        convert_timestamp_to_playback_time, get_timestamp)
from youtube_interface import (get_broadcast_data, get_youtube_credentials,
                               update_broadcast_description)

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HOTKEY_ID_ARRAY = []
HOTKEY_NAMES_BY_ID = {}
SCRIPT_SETTINGS = {
    # todo combine this and stream service
    'output_type': None,
    'stream_service': None,
    'start_time': None,
    'start_timestamp': None,
    'last_timestamp': '00:00:00',
    'credentials': None,
    'timestamp_group_range': 0,
}


def determine_streaming_service(stream_url):
    """Use obs service type to determine stream service.
    """
    streaming_service = None

    if 'youtube' in stream_url:
        streaming_service = 'youtube'
    # The check for twitch feels weak, but I found it on a twitch website
    # https://help.twitch.tv/s/twitch-ingest-recommendation?language=en_US
    elif 'live-video' in stream_url:
        streaming_service = 'twitch'

    return streaming_service

# callback functions
# ------------------------------------------------------------


def hotkey_callback(button_down: bool):
    """Handle OBS hotkey press as callback function.
    """
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    if button_down:
        current_timestamp = get_timestamp('float')
        stream_marker = current_timestamp - SCRIPT_SETTINGS['start_timestamp']
        stream_marker = convert_timestamp_to_playback_time(stream_marker)
        logging.info(f'stream_marker: {stream_marker}')

        broadcast_data = get_broadcast_data(SCRIPT_SETTINGS['credentials'])

        time_since_last_stream_marker = convert_playback_time_to_timestamp(
            stream_marker
        ) - convert_playback_time_to_timestamp(SCRIPT_SETTINGS['last_timestamp'])  # type: ignore
        logging.debug(
            (
                f'timestamp_group_range: {SCRIPT_SETTINGS["timestamp_group_range"]}\n'
                f'seconds since last marker: {time_since_last_stream_marker.total_seconds()}'
            )
        )
        if (time_since_last_stream_marker.total_seconds() <=
                SCRIPT_SETTINGS['timestamp_group_range']):
            logging.info(
                'Prevented writing stream marker, too close to previous marker'
            )

            return

        new_description = (
            f'{broadcast_data.broadcast_description}\n'
            f'{stream_marker} - \n'
        )
        logging.info('Adding new stream marker to description')
        update_broadcast_description(
            SCRIPT_SETTINGS['credentials'],
            broadcast_data,
            new_description,
        )

        SCRIPT_SETTINGS['last_timestamp'] = stream_marker


def on_event_callback(event):
    """Handle OBS frontend events as callback function.

    List of events can be found here: https://docs.obsproject.com/reference-frontend-api
    """
    # pylint: disable=global-variable-not-assigned
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
        SCRIPT_SETTINGS['last_timestamp'] = '00:00:00'
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STARTED:
        SCRIPT_SETTINGS['output_type'] = 'recording'
    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPED:
        SCRIPT_SETTINGS['output_type'] = None
    elif event == obs.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        SCRIPT_SETTINGS['output_type'] = None


# ------------------------------------------------------------

# OBS library hooks
# ------------------------------------------------------------


# todo update this
def script_description():
    """OBS hook that setups up script description in OBS UI.
    """
    description = ''
    description += '<b>Create stream markers</b>'
    description += '<hr>'
    description += 'Script adds the ability to set a hotkey to save a timestamp to a file. '
    description += "The file's name will correspond to the start time of the stream."
    description += 'Script will only create markers if streaming or recording.'
    description += '<hr>'
    description += '<b>Settings</b>'
    description += '<hr>'
    description += '<b>Debug mode</b> enables debug settings and prints used for development.'
    description += '<br>'
    description += '<b>Range to group timestamps</b> '
    description += 'prevents creating stream markers too close to each other. '
    description += 'The value is in seconds and specifies the minimum time between stream markers'
    description += '<hr>'

    return description


def script_properties():
    """OBS hook that setups script settings in OBS UI.
    """
    props = obs.obs_properties_create()

    # enable script's debug mode
    obs.obs_properties_add_bool(props, 'debug_enabled', 'Debug mode')

    obs.obs_properties_add_int(
        props,
        'group_timestamp_range',
        'Range to group timestamps',
        0,
        10000,
        1,
    )

    return props


def script_save(settings):
    """OBS hook called when script is being saved.
    """
    # save hotkeys in script properties
    for hotkey_id in HOTKEY_ID_ARRAY:
        # save each hotkeys data_array into script settings by the hotkeys name
        obs.obs_data_set_array(
            settings,
            HOTKEY_NAMES_BY_ID[hotkey_id],
            obs.obs_hotkey_save(hotkey_id),
        )


def script_load(settings):
    """OBS hook that runs when script first loads or reloaded.
    """
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    print(f'--- {__file__} loaded ---')

    # handle OBS frontend events
    obs.obs_frontend_add_event_callback(on_event_callback)

    def hotkey_callback_args(button_down):
        """hack to pass additional arguments to callback function
        """
        return hotkey_callback(button_down)
    HOTKEY_ID_ARRAY.append(obs.obs_hotkey_register_frontend(
        'SHORTCUT 1',
        'Scripts - create_stream_markers.py - Push create stream marker',
        hotkey_callback_args
    )
    )
    HOTKEY_NAMES_BY_ID[HOTKEY_ID_ARRAY[len(HOTKEY_ID_ARRAY)-1]] = 'SHORTCUT 1'

    # load hotkeys from script save file
    for hotkey_id in HOTKEY_ID_ARRAY:
        # todo find way to use obs_hotkey_get_name instead of tracking the name manually
        # get the hotkeys data_array from the script settings (was saved under the hotkeys name)
        hotkey_data_array_from_settings = obs.obs_data_get_array(
            settings,
            HOTKEY_NAMES_BY_ID[hotkey_id],
        )
        # load the saved hotkeys data_array to the new created hotkey associated with the hotkey_id
        obs.obs_hotkey_load(hotkey_id, hotkey_data_array_from_settings)

        obs.obs_data_array_release(hotkey_data_array_from_settings)

    # todo make this a obs variable
    token_path = pathlib.Path(
        'C:/Users/denni/Desktop/Programming/youtube-stream-markers/src/token.json'
    )
    # todo only run this when stream starts
    SCRIPT_SETTINGS['credentials'] = get_youtube_credentials(
        token_path
    )


def script_update(settings):
    """OBS hook thats called whenever script settings get changed in OBS
    """
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    if obs.obs_data_get_bool(settings, 'debug_enabled'):
        logging.root.setLevel(logging.DEBUG)
        SCRIPT_SETTINGS['start_time'] = get_timestamp('string')
        SCRIPT_SETTINGS['start_timestamp'] = get_timestamp('float')
    else:
        logging.root.setLevel(logging.CRITICAL)
        SCRIPT_SETTINGS['start_time'] = None
        SCRIPT_SETTINGS['start_timestamp'] = None

    SCRIPT_SETTINGS['timestamp_group_range'] = obs.obs_data_get_int(
        settings,
        'group_timestamp_range'
    )

# ------------------------------------------------------------
