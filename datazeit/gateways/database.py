import abc
from abc import ABC
from typing import Dict, List

from clickhouse_driver import Client

from datazeit.config import config


class DatabaseGateway(ABC):
    @abc.abstractmethod
    def get_products(self, p_c_id: str) -> "Product":
        raise NotImplementedError

    @abc.abstractmethod
    def get_ingredients(self, p_e_id: str) -> List["Ingredient"]:
        raise NotImplementedError


class ClickHouseGateway(DatabaseGateway):
    def __init__(self, client: Client = None):

        self._client = client or Client(**config["database-conf"].get(dict))

    def get_products(self, p_c_id: str) -> "Product":
        query = f"""
            SELECT 
                * 
            FROM products
            WHERE p_c_id = '{p_c_id}' 
        """
        results = self._client.execute(query)

        return results

    def get_ingredients(self, p_e_id: str) -> List["Ingredient"]:
        pass
