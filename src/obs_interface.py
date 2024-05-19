# pylint: disable-next=import-error
import obspython as obs


class ObsInterface:
    def __init__(self) -> None:
        pass

    def script_description(self) -> str:
        """OBS hook that setups up script description in OBS UI."""
        print(f'{__file__} script_description()')
        description = f'description from {__file__}'

        return description

    def script_properties(self):
        print(f'{__file__} script_properties()')

        props = obs.obs_properties_create()
        # int input box determining how long to ignore timestamps if placed too close together
        obs.obs_properties_add_int(
            props,
            'group_timestamp_range',
            'Range to group timestamps',
            0,
            10000,
            1,
        )

    def script_save(self, settings):
        print(f'{__file__} script_save()')

    def script_load(self, settings):
        print(f'{__file__} script_load()')

    def script_update(self, settings):
        print(f'{__file__} script_update()')
