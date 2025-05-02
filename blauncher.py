import sys
import subprocess
import os
import re
from pathlib import Path

DEFAULT_BLENDER_VERSION = "4.4"


def parse_version(argv: list[str]) -> tuple[str, list[str]]:
    """
    :return: Tuple of version and left out arguments.
    """
    # TODO: Ideally Blender Launcher should be able to work without version
    # provided but currently it does not.
    VERSION_PATTERN = r"-(\d.\d+)"
    if not argv or not (re_match := re.match(VERSION_PATTERN, argv[0])):
        return DEFAULT_BLENDER_VERSION, argv
    version = re_match.group(1)
    return version, argv[1:]


def main():
    repo_location = os.environ.get("BLENDER_LAUNCHER_REPO")
    if repo_location is None:
        raise Exception("'BLENDER_LAUNCHER_REPO' environment variable is not set.")
    repo_location = Path(repo_location)
    main_script = repo_location / "source" / "main.py"
    assert main_script.exists(), main_script

    argv = sys.argv[1:]
    version, blender_args = parse_version(argv)

    args = [
        "python",
        str(main_script),
        "launch",
        "--version",
        version + ".^",
        "--cli",
    ]
    if blender_args:
        args.append("--")
        args.extend(blender_args)
    process = subprocess.run(args, cwd=repo_location)
    exit(process.returncode)


if __name__ == "__main__":
    main()
