import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_BLENDER_VERSION = "5.0"


def parse_version(argv: list[str]) -> tuple[str, list[str]]:
    """
    :return: Tuple of version and left out arguments.
    """
    # TODO: Ideally Blender Launcher should be able to work without version
    # provided but currently it does not.
    VERSION_PATTERN_2 = r"^-(\d+.\d+)$"
    VERSION_PATTERN_3 = r"^-(\d+.\d+.\d+)$"
    if not argv or not (re_match := (re.match(VERSION_PATTERN_2, argv[0]) or re.match(VERSION_PATTERN_3, argv[0]))):
        return DEFAULT_BLENDER_VERSION, argv
    version = re_match.group(1)
    return version, argv[1:]


def main():
    # Environment variable here is only for the case if need to test dev version.
    # Putting executable in PATH is preferred way.
    repo_location = os.environ.get("BLENDER_LAUNCHER_REPO")
    if repo_location is not None:
        repo_location = Path(repo_location)
        main_script = repo_location / "source" / "main.py"
        assert main_script.exists(), main_script
        blender_launcher_command = [sys.executable, str(main_script)]
    else:
        executable_name = "Blender Launcher"
        blender_launcher_path = shutil.which(executable_name)
        if blender_launcher_path is None:
            raise Exception(
                f"Couldn't find Blender Launcher executable ({executable_name}) in PATH "
                "and 'BLENDER_LAUNCHER_REPO' environment variable is not set."
            )
        blender_launcher_command = [blender_launcher_path]

    argv = sys.argv[1:]
    version, blender_args = parse_version(argv)
    if version.count(".") == 1:
        version += ".^"

    args = [
        *blender_launcher_command,
        "launch",
        "--version",
        version,
        "--cli",
    ]
    if blender_args:
        args.append("--")
        args.extend(blender_args)
    process = subprocess.run(args)
    exit(process.returncode)


if __name__ == "__main__":
    main()
