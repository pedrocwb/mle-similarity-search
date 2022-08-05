import os
from pathlib import Path
import confuse


ROOT_DIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)
config = confuse.Configuration("datazeit", __name__)
