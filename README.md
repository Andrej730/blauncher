### BLauncher

Simple script to start Blender Launcher with specific version of Blender.

blauncher acts exactly as if Blender was started directly,
except it has additional optional first argument `version`
that allows specifying Blender version to start
(`py -x.x` inspired).

`version` is a double digit version string provided in the format: `-x.y`.

Example usage:
```sh
python blauncher.py -4.4 --background
```

Ideally it should be set up to be globally available as `blender`:
```sh
blender -4.4 --background
blender --background
```

### Setup

Ensure to set `BLENDER_LAUNCHER_REPO` enviroment variable to Blender Launcher repo:
- https://github.com/Andrej730/Blender-Launcher-V2/tree/launch-blender-args

Currently default Blender version to start when version argument is not provided
is hardcoded as `DEFAULT_BLENDER_VERSION`.
