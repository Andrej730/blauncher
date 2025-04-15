import sys
import subprocess
import os
from pathlib import Path


def main():
    # TODO: add default Blender version.
    repo_location = os.environ.get("BLENDER_LAUNCHER_REPO")
    if repo_location is None:
        raise Exception("'BLENDER_LAUNCHER_REPO' environment variable is not set.")
    repo_location = Path(repo_location)
    main_script = repo_location / "source" / "main.py"
    assert main_script.exists(), main_script

    argv = sys.argv[1:]
    assert len(argv) >= 1
    assert argv[0].startswith("-")
    version = argv[0].removeprefix("-")
    blender_args = argv[1:]
    args = [
        "python",
        str(main_script),
        "launch",
        "--version",
        version + ".*",
        "--cli",
    ]
    if blender_args:
        args.extend(blender_args)
    process = subprocess.run(args, cwd=repo_location)
    exit(process.returncode)


if __name__ == "__main__":
    main()
