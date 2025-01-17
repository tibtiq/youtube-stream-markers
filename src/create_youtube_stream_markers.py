"""This module is an OBS script that creates stream markers for a youtube livestream.

The stream markers are placed in the description of the livestream.
"""


import logging
import pathlib
from datetime import datetime

# pylint: disable-next=import-error
import obspython as obs

from stream_marker import StreamMarker
from youtube_interface import (get_broadcast_data, get_youtube_credentials,
                               update_broadcast_description)

logger = logging.getLogger(__file__)

HOTKEY_ID_ARRAY = []
HOTKEY_NAMES_BY_ID = {}
SCRIPT_SETTINGS = {
    'start_stream_marker': None,
    'last_stream_marker': None,
    'credentials': None,
    'credentials_path': None,
    'stream_marker_group_range': 0,
    'stream_marker_offset': 0,
    'first_stream_marker_label': 'Start'
}


def setup_logging(log_level: int, log_dir: pathlib.Path) -> None:
    log_level = 50 - (log_level * 10)
    formatter = logging.Formatter(
        fmt='%(asctime)s |  %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    # todo cleanup logs

    global logger
    logger = logging.getLogger(__file__)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)

    log_dir = log_dir.resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    log_file = log_dir / f'{now.strftime("%Y-%m-%d %H-%M-%S")}.log'

    file_handler = logging.FileHandler(filename=log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


# callback functions
# ------------------------------------------------------------


def hotkey_callback(button_down: bool):
    """Handle OBS hotkey press as callback function."""
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    if button_down:
        if SCRIPT_SETTINGS['start_stream_marker'] is None:
            print('Prevented creating stream marker, not streaming')
            return

        current_stream_marker = StreamMarker()

        # todo replace this so it only applies if offset is not 0, same with the resulting log
        logger.debug(f'stream_marker before offset: {current_stream_marker}')
        current_stream_marker -= SCRIPT_SETTINGS['stream_marker_offset']

        logger.info(f'stream_marker after offset: {current_stream_marker}')

        broadcast_data = get_broadcast_data(SCRIPT_SETTINGS['credentials'])

        time_since_last_stream_marker = 0
        if SCRIPT_SETTINGS['last_stream_marker'] is not None:
            time_since_last_stream_marker = current_stream_marker - \
                SCRIPT_SETTINGS['last_stream_marker']
        logger.debug(
            f'stream_marker_group_range: {SCRIPT_SETTINGS["stream_marker_group_range"]}'
        )
        logger.debug(
            f'seconds since last marker: {time_since_last_stream_marker}'
        )

        if 0 < time_since_last_stream_marker <= SCRIPT_SETTINGS['stream_marker_group_range']:
            logger.info('Prevented writing stream marker, too close to previous marker')
            return

        new_description = (
            f'{broadcast_data.broadcast_description}\n'
            f'{current_stream_marker.as_playback_time(SCRIPT_SETTINGS["start_stream_marker"])} - \n'
        )
        logger.info('Adding new stream marker to description')
        update_broadcast_description(
            SCRIPT_SETTINGS['credentials'],
            broadcast_data,
            new_description,
        )

        SCRIPT_SETTINGS['last_stream_marker'] = current_stream_marker


def on_event_callback(event):
    """Handle OBS frontend events as callback function.

    List of events can be found here: https://docs.obsproject.com/reference-frontend-api
    """
    # pylint: disable=global-variable-not-assigned
    global SCRIPT_SETTINGS

    # determine if streaming or recording and started or stopped
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTED:
        SCRIPT_SETTINGS['start_stream_marker'] = StreamMarker()
        SCRIPT_SETTINGS['last_stream_marker'] = None

        broadcast_data = get_broadcast_data(SCRIPT_SETTINGS['credentials'])
        update_broadcast_description(
            SCRIPT_SETTINGS['credentials'],
            broadcast_data,
            f'00:00:00 - {SCRIPT_SETTINGS["first_stream_marker_label"]}',
        )


# ------------------------------------------------------------

# OBS library hooks
# ------------------------------------------------------------


def script_description():
    """OBS hook that setups up script description in OBS UI."""
    description = (
        '<b>Create Youtube stream markers</b>'
        '<hr>'
        'Script adds the ability to set a hotkey to save a stream marker in the description'
        'of a Youtube livestream. '
        '<hr>'
        '<b>Settings</b>'
        '<hr>'
        '<b>Credentials file path</b> is the path to your Youtube API credentials file. '
        'Refer to README.md regarding generating this file.'
        '<br>'
        '<b>Range to group stream markers</b> prevents creating stream markers too close to '
        'each other. The value is in seconds and specifies the minimum time between '
        'stream markers.'
        '<br>'
        '<b>stream marker offset</b> offsets stream markers from when they created by the '
        "specified number of seconds. This is helpful when processing stream markers as "
        "they're usually created after a 'moment' happens. The offset is towards before"
        "the 'moment' happens."
        '<br>'
        '<b>First stream marker label</b> Label to put for first auto generated stream marker.'
        'The marker is 00:00:00 and is required for chapters to work on Youtube.'
        " Defaults to 'Start'."
        '<br>'
        '<b>Debug mode</b> enables debug settings and prints used for development. '
        'When not streaming, stream markers will be added to the description of last '
        'stream. '
        '<hr>'
    )
    # todo add info that logs are created in script location

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

    # int input box determining how long to ignore stream markers if placed too close together
    obs.obs_properties_add_int(
        props,
        'group_stream_marker_range',
        'Range to group stream markers',
        0,
        10000,
        1,
    )

    # int input box specifying the offset to subtract from when a stream marker is created
    obs.obs_properties_add_int(
        props,
        'stream_marker_offset',
        'stream_marker offset',
        0,
        10000,
        1,
    )

    # str input box specifying the label for the auto generated stream marker
    obs.obs_properties_add_text(
        props,
        'first_stream_marker_label',
        'First stream marker label',
        obs.OBS_TEXT_DEFAULT
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
    setup_logging(logging.CRITICAL, pathlib.Path(__file__).parent.parent / 'logs')

    # handle OBS frontend events
    obs.obs_frontend_add_event_callback(on_event_callback)

    HOTKEY_ID_ARRAY.append(obs.obs_hotkey_register_frontend(
        'SHORTCUT 1',
        'Scripts - create_stream_markers.py - Push create stream marker',
        hotkey_callback
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
        logger.setLevel(logging.DEBUG)
        SCRIPT_SETTINGS['start_stream_marker'] = StreamMarker()
    else:
        logger.setLevel(logging.CRITICAL)
        SCRIPT_SETTINGS['start_stream_marker'] = None

    SCRIPT_SETTINGS['stream_marker_group_range'] = obs.obs_data_get_int(
        settings,
        'group_stream_marker_range'
    )

    SCRIPT_SETTINGS['stream_marker_offset'] = obs.obs_data_get_int(
        settings,
        'stream_marker_offset'
    )

    SCRIPT_SETTINGS['first_stream_marker_label'] = obs.obs_data_get_string(
        settings,
        'first_stream_marker_label'
    )

    # only load new credentials if credentials path has changed
    if (
        obs.obs_data_get_string(settings, 'credentials_file_path',) !=
        SCRIPT_SETTINGS['credentials_path']
    ):
        logger.info('Loading credentials because a new credentials path was provided')
        SCRIPT_SETTINGS['credentials_path'] = obs.obs_data_get_string(
            settings,
            'credentials_file_path',
        )
        SCRIPT_SETTINGS['credentials'] = get_youtube_credentials(
            pathlib.Path(obs.obs_data_get_string(settings, 'credentials_file_path'))
        )
# ------------------------------------------------------------
