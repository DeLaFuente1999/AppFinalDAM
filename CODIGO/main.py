from pathlib import Path
import pathlib
import subprocess
import os
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

absolutepath = str(pathlib.Path().resolve())

if __name__ == '__main__':
    subprocess.call(['python', os.path.join(absolutepath, 'CODIGO\\LOGIN\\login.py')])
