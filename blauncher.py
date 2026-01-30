import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_BLENDER_VERSION = "5.1"


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
    # Using "Blender Launcher" executable from PATH would be more convenient
    # but there's an issue when you do
    # `"Blender Launcher.exe" launch --version X.Y.Z --cli`
    # It launches Blender in a separate process and you won't be able to see the logs
    # in the terminal where you executed the command.
    # It's some kind of PyInstaller limitation:
    # https://github.com/Victor-IX/Blender-Launcher-V2/issues/242
    repo_location = os.environ.get("BLENDER_LAUNCHER_REPO")
    if repo_location is None:
        raise Exception("'BLENDER_LAUNCHER_REPO' environment variable is not set.")
    repo_location = Path(repo_location)
    main_script = repo_location / "source" / "main.py"
    assert main_script.exists(), main_script

    argv = sys.argv[1:]
    version, blender_args = parse_version(argv)
    if version.count(".") == 1:
        version += ".^"

    # Using `uv` instead of `python` to avoid installing all Blender Launcher dependencies globally.
    # `uv run` will automatically detect venv in the current folder and use it.
    args = [
        "uv",
        "run",
        str(main_script),
        "launch",
        "--version",
        version,
        "--cli",
    ]
    if blender_args:
        args.append("--")
        args.extend(blender_args)
    process = subprocess.run(args, cwd=repo_location)
    exit(process.returncode)


if __name__ == "__main__":
    main()
