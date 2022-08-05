import abc
import dataclasses
from abc import ABC
from typing import Dict, List

from clickhouse_driver import Client

from datazeit.config import config


@dataclasses.dataclass
class Product:
    p_c_id: int
    brand: str
    title: str
    product_type: str
    p_e_ids: List[int]


class DatabaseGateway(ABC):
    @abc.abstractmethod
    def get_product_by_variation(self, p_e_id: str) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def get_ingredients(self, p_e_id: str) -> List["Ingredient"]:
        raise NotImplementedError


class ClickHouseGateway(DatabaseGateway):
    def __init__(self, client: Client = None):
        self._client = client or Client(**config["database-conf"].get(dict))

    def get_product_by_variation(self, p_e_id: str) -> "Product":
        query = """
            SELECT 
                p_c_id, 
                brand, 
                title, 
                product_type,
                p_e_ids
            FROM products
            WHERE arrayExists(x-> x = %(p_e_id)s, p_e_ids) = 1; 
        """
        result = self._client.execute(query, {"p_e_id": p_e_id})[0]

        return Product(
            p_c_id=result[0],
            brand=result[1],
            title=result[2],
            product_type=result[3],
            p_e_ids=result[4],
        )

    def get_ingredients(self, p_e_id: str) -> List["Ingredient"]:
        pass
