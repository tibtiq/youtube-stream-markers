import logging
import pathlib
from typing import Type

# pylint: disable-next=import-error
import obspython as obs
from obs_interface import ObsInterface

OBS_INTERFACE = ObsInterface()


def script_description() -> str:
    """OBS hook that setups up script description in OBS UI."""
    print(f'{__file__} script_description()')

    return OBS_INTERFACE.script_description()


def script_properties() -> None:
    print(f'{__file__} script_properties()')
    OBS_INTERFACE.script_description()


def script_save(settings) -> None:
    """# todo _summary_

    Args:
        settings: SwigPyObject
            Data containing settings for the script.

            SWIG object used to connect OBS C/C++ libraries to scripting languages.
            Refer to docs/develop.md for more information about
    """
    print(f'{__file__} script_save()')
    OBS_INTERFACE.script_save(settings)


def script_load(settings) -> None:
    """# todo _summary_

    Args:
        settings: SwigPyObject
            Data containing settings for the script.

            SWIG object used to connect OBS C/C++ libraries to scripting languages.
            Refer to docs/develop.md for more information about
    """
    print(f'{__file__} script_load()')
    print(settings)
    print(type(settings))
    OBS_INTERFACE.script_load(settings)


def script_update(settings) -> None:
    """# todo _summary_

    Args:
        settings: SwigPyObject
            Data containing settings for the script.

            SWIG object used to connect OBS C/C++ libraries to scripting languages.
            Refer to docs/develop.md for more information about
    """
    print(f'{__file__} script_update()')
    OBS_INTERFACE.script_update(settings)
