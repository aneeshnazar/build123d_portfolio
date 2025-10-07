from jupyterlab.labapp import main as jupyterlaunch
import sys
from pathlib import Path

def run():
    cfg_path = str(Path(__file__).parent / "jupyter_lab_config.py")
    sys.exit(jupyterlaunch(["--config", cfg_path]))