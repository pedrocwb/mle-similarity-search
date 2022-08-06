import os
from collections import OrderedDict
from pathlib import Path
import confuse
from dotenv import load_dotenv

load_dotenv("../.env")

ROOT_DIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)
config = confuse.Configuration("datazeit", __name__)

db_config = config["database"].get()
db_config["user"] = os.environ["CLICKHOUSE_USER"]
db_config["password"] = os.environ["CLICKHOUSE_PASSWORD"]

config["database"] = OrderedDict(db_config)
