"""A convenience script to launch Blender Launcher itself.

Since we're stuck without executable and with `BLENDER_LAUNCHER_REPO` environment variable,
got to make it easier to launch Blender Launcher from terminal.
"""

import os
import shutil
import subprocess
from pathlib import Path

UV = shutil.which("uv")
assert UV, "Could not find 'uv' executable in PATH."

repo_location = os.environ.get("BLENDER_LAUNCHER_REPO")
if repo_location is None:
    raise Exception("'BLENDER_LAUNCHER_REPO' environment variable is not set.")
repo_location = Path(repo_location)
main_script = repo_location / "source" / "main.py"

# Use UV to automatically pick up local venv.
subprocess.check_call([UV, "run", str(repo_location / "build_style.py")], cwd=repo_location)
subprocess.check_call([UV, "run", str(main_script)], cwd=repo_location)
