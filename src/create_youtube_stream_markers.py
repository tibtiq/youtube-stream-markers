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
from timestamp import Timestamp
from youtube_interface import (
    get_broadcast_data,
    get_youtube_credentials,
    update_broadcast_description,
)

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

HOTKEY_ID_ARRAY = []
HOTKEY_NAMES_BY_ID = {}
SCRIPT_SETTINGS = {
    'start_timestamp': None,
    'last_timestamp': None,
    'credentials': None,
    'credentials_path': None,
    'timestamp_group_range': 0,
    'timestamp_offset': 0,
}


# callback functions
# ------------------------------------------------------------


def hotkey_callback(button_down: bool):
    """Handle OBS hotkey press as callback function."""
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    if button_down:
        if SCRIPT_SETTINGS['start_timestamp'] is None:
            print('Prevented creating stream marker, not streaming')
            return

        current_timestamp = Timestamp()

        logging.debug(f'stream_marker before offset: {current_timestamp}')
        current_timestamp -= SCRIPT_SETTINGS['timestamp_offset']

        logging.info(f'stream_marker after offset: {current_timestamp}')

        broadcast_data = get_broadcast_data(SCRIPT_SETTINGS['credentials'])

        time_since_last_stream_marker = current_timestamp - SCRIPT_SETTINGS['last_timestamp']
        logging.debug(
            (
                f'timestamp_group_range: {SCRIPT_SETTINGS["timestamp_group_range"]}\n'
                f'seconds since last marker: {time_since_last_stream_marker}'
            )
        )
        if (0 < time_since_last_stream_marker <= SCRIPT_SETTINGS['timestamp_group_range']):
            logging.info('Prevented writing stream marker, too close to previous marker')
            return

        new_description = (
            f'{broadcast_data.broadcast_description}\n'
            f'{current_timestamp.as_playback_time(SCRIPT_SETTINGS["start_timestamp"])} - \n'
        )
        logging.info('Adding new stream marker to description')
        update_broadcast_description(
            SCRIPT_SETTINGS['credentials'],
            broadcast_data,
            new_description,
        )

        SCRIPT_SETTINGS['last_timestamp'] = current_timestamp


def on_event_callback(event):
    """Handle OBS frontend events as callback function.

    List of events can be found here: https://docs.obsproject.com/reference-frontend-api
    """
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    # determine if streaming or recording and started or stopped
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        SCRIPT_SETTINGS['start_timestamp'] = Timestamp()
        SCRIPT_SETTINGS['last_timestamp'] = None


# ------------------------------------------------------------

# OBS library hooks
# ------------------------------------------------------------


def script_description():
    """OBS hook that setups up script description in OBS UI."""
    description = ''
    description += '<b>Create Youtube stream markers</b>'
    description += '<hr>'
    description += 'Script adds the ability to set a hotkey to save a timestamp in the description'
    description += 'of a Youtube livestream. '
    description += '<hr>'
    description += '<b>Settings</b>'
    description += '<hr>'
    description += '<b>Credentials file path</b> is the path to your Youtube API credentials file. '
    description += 'Refer to README.md regarding generating this file.'
    description += '<br>'
    description += '<b>Range to group timestamps</b> prevents creating stream markers too close to '
    description += 'each other. The value is in seconds and specifies the minimum time between '
    description += 'stream markers.'
    description += '<br>'
    description += '<b>Timestamp offset</b> offsets timestamps from when they created by the '
    description += "specified number of seconds. This is helpful when processing timestamps as "
    description += "they're usually created after a 'moment' happens. The offset is towards before"
    description += "the 'moment' happens."
    description += '<br>'
    description += '<b>Debug mode</b> enables debug settings and prints used for development. '
    description += 'When not streaming, stream markers will be added to the description of last '
    description += 'stream. '
    description += '<hr>'

    return description


def script_properties():
    """OBS hook that setups script settings in OBS UI."""
    props = obs.obs_properties_create()

    # file browse for youtube api credentials file
    obs.obs_properties_add_path(
        props,
        'credentials_file_path',
        'Credentials file path:',
        obs.OBS_PATH_FILE,
        "*.json",
        "",
    )

    # int input box determining how long to ignore timestamps if placed too close together
    obs.obs_properties_add_int(
        props,
        'group_timestamp_range',
        'Range to group timestamps',
        0,
        10000,
        1,
    )

    # int input box specifying the offset to subtract from when a timestamp is created
    obs.obs_properties_add_int(
        props,
        'timestamp_offset',
        'Timestamp offset',
        0,
        10000,
        1,
    )

    # checkbox to enable script's debug mode
    obs.obs_properties_add_bool(props, 'debug_enabled', 'Debug mode')

    return props


def script_save(settings):
    """OBS hook called when script is being saved."""
    # save hotkeys in script properties
    for hotkey_id in HOTKEY_ID_ARRAY:
        # save each hotkeys data_array into script settings by the hotkeys name
        obs.obs_data_set_array(
            settings,
            HOTKEY_NAMES_BY_ID[hotkey_id],
            obs.obs_hotkey_save(hotkey_id),
        )


def script_load(settings):
    """OBS hook that runs when script first loads or reloaded."""
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    print(f'--- {__file__} loaded ---')

    # handle OBS frontend events
    obs.obs_frontend_add_event_callback(on_event_callback)

    def hotkey_callback_args(button_down):
        """Hack to pass additional arguments to callback function."""
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

    # todo only run this when stream starts
    SCRIPT_SETTINGS['credentials_path'] = obs.obs_data_get_string(settings, 'credentials_file_path')
    SCRIPT_SETTINGS['credentials'] = get_youtube_credentials(
        pathlib.Path(SCRIPT_SETTINGS['credentials_path'])
    )


def script_update(settings):
    """OBS hook thats called whenever script settings get changed in OBS.

    This function is also run immediately after script_load() when OBS is opening.

    """
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    if obs.obs_data_get_bool(settings, 'debug_enabled'):
        logging.root.setLevel(logging.DEBUG)
        SCRIPT_SETTINGS['start_timestamp'] = Timestamp()
    else:
        logging.root.setLevel(logging.CRITICAL)
        SCRIPT_SETTINGS['start_timestamp'] = None

    SCRIPT_SETTINGS['timestamp_group_range'] = obs.obs_data_get_int(
        settings,
        'group_timestamp_range'
    )

    SCRIPT_SETTINGS['timestamp_offset'] = obs.obs_data_get_int(
        settings,
        'timestamp_offset'
    )

    # only load new credentials if credentials path has changed
    if (
        obs.obs_data_get_string(settings, 'credentials_file_path',) !=
        SCRIPT_SETTINGS['credentials_path']
    ):
        logging.info('Loading credentials because a new credentials path was provided')
        SCRIPT_SETTINGS['credentials_path'] = obs.obs_data_get_string(
            settings,
            'credentials_file_path',
        )
        SCRIPT_SETTINGS['credentials'] = get_youtube_credentials(
            pathlib.Path(obs.obs_data_get_string(settings, 'credentials_file_path'))
        )
# ------------------------------------------------------------
