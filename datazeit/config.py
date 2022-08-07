import os
from collections import OrderedDict
from pathlib import Path
import confuse
from dotenv import load_dotenv

load_dotenv("../.env")

ROOT_DIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)
config = confuse.Configuration("datazeit", __name__)
