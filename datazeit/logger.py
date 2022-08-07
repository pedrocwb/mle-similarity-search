import logging
from logging import getLogger


logging.basicConfig(
    filename="datazeit-api.log",
    level=logging.DEBUG,
    format="%(asctime)s %(name)s: %(levelname)s - %(message)s",
)
logger = getLogger(__name__)
