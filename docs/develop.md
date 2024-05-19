# What is the variable `settings`?
As documented by the OBS team

> The values of the data settings available in `settings` during OBS startup reflect the state saved
> at previous OBS closure (properties changed by the user), and are already set in settings when
> script_defaults, script_load and script_update are called

The `settings` is saved/loaded to/from a json file. Which can be viewed at the following paths.

Windows
```
%AppData%\obs-studio\basic\scenes\Untitled_2.json
```


# Resources
- [OBS library interface](https://docs.obsproject.com/scripting#script-function-exports)
- [OBS documentation about settings variable](<https://obsproject.com/wiki/Getting-Started-With-OBS-Scripting#:~:text=settings%2C%20see%20below)-,Please%20note%20that%3A,-The%20values%20of>)