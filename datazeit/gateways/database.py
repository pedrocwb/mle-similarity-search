import abc
import dataclasses
import os
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


@dataclasses.dataclass
class Ingredient:
    p_e_id: int
    ingr_id: int
    inci_name: str


class DatabaseGateway(ABC):
    @abc.abstractmethod
    def get_product_by_variation(self, p_e_id: str) -> Product:
        raise NotImplementedError

    @abc.abstractmethod
    def get_products(self) -> List[Product]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_ingredients(self) -> List[Ingredient]:
        raise NotImplementedError


class ClickHouseGateway(DatabaseGateway):
    def __init__(self, client: Client = None):
        user = os.environ["CLICKHOUSE_USER"]
        password = os.environ["CLICKHOUSE_PASSWORD"]
        host = os.environ["CLICKHOUSE_HOST"]

        self._client = client or Client(
            host=host, user=user, password=password, **config["database"].get(dict)
        )

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

    def get_products(self) -> List[Product]:
        query = """
            SELECT 
                p_c_id, 
                brand, 
                title, 
                product_type,
                p_e_ids
            FROM products
        """
        result = self._client.execute(query)

        return [
            Product(
                p_c_id=prod[0],
                brand=prod[1],
                title=prod[2],
                product_type=prod[3],
                p_e_ids=prod[4],
            )
            for prod in result
        ]

    def get_ingredients(self) -> List[Ingredient]:
        query = """
            SELECT 
                p_e_id, 
                ingr_id,
                inci_name
            FROM ingredients
        """
        result = self._client.execute(query)

        return [
            Ingredient(p_e_id=ing[0], ingr_id=ing[1], inci_name=ing[2])
            for ing in result
        ]
