import abc
from abc import ABC
from typing import Any, Dict, List

import requests as requests
from requests import RequestException

from datazeit.config import config
from datazeit.logger import logger


class SearchEngineGateway(ABC):
    @abc.abstractmethod
    def search(self, index: str, search_term: str) -> Dict[Any, Any]:
        raise NotImplementedError


class QuickWitGateway(SearchEngineGateway):
    def __init__(self):
        self._search_url = config["search_engine"]["url"].get(str)

    def search(self, index: str, search_term: str) -> Dict[Any, Any]:
        query = f"{'+AND+'.join(search_term.split( ))}"
        data = self._make_request(query, index)

        return data

    def _make_request(self, query: str, index: str) -> Dict[Any, Any]:

        try:
            # TODO: this is inefficient. Needs refactoring.
            request_url = f"{self._search_url}/{index}/search?query={query}"
            data = requests.get(request_url, params={"max_hits": 0})
            num_hits = data.json()["num_hits"]

            data = requests.get(request_url, params={"max_hits": num_hits})
            data = data.json()

        except RequestException as e:
            logger.debug(f"Error querying for search terms: {e}")
            raise
        return data
