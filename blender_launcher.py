"""A convenience script to launch Blender Launcher itself.

Since we're stuck without executable and with `BLENDER_LAUNCHER_REPO` environment variable,
got to make it easier to launch Blender Launcher from terminal.
"""

import os
import subprocess
import sys
from pathlib import Path

repo_location = os.environ.get("BLENDER_LAUNCHER_REPO")
if repo_location is None:
    raise Exception("'BLENDER_LAUNCHER_REPO' environment variable is not set.")
repo_location = Path(repo_location)
main_script = repo_location / "source" / "main.py"
subprocess.check_call([sys.executable, str(main_script)], cwd=repo_location)
