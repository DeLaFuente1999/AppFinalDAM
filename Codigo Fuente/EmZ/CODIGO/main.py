import pathlib
import subprocess
import sys
import os
from pathlib import Path

absolutepath1 = str(pathlib.Path().resolve())
absolutepath = os.path.abspath(__file__)


subprocess.call(['python', os.path.join(absolutepath, '..\\LOGIN\\login.py')])