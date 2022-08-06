from unittest.mock import MagicMock

import pytest
from clickhouse_driver import Client

from datazeit.gateways.database import ClickHouseGateway, Product


@pytest.fixture
def sql_product_results():
    return [
        (
            34566,
            "Dr Irena Eris",
            "Anti-Falten-Tagescreme",
            "Day cream",
            [5744705805828983682, -9221563774004008904],
        )
    ]


def test_get_products(sql_product_results):
    gtw = ClickHouseGateway(client=Client.from_url("clickhouse://host"))
    gtw._client.execute = MagicMock(return_value=sql_product_results)
    p_e_id = "5744705805828983682"

    product = gtw.get_product_by_variation(p_e_id=p_e_id)

    gtw._client.execute.assert_called()
    assert isinstance(product, Product)
    assert product.p_c_id == sql_product_results[0][0]
    assert product.brand == sql_product_results[0][1]
    assert product.title == sql_product_results[0][2]
    assert product.product_type == sql_product_results[0][3]
    assert product.p_e_ids == sql_product_results[0][4]
    assert int(p_e_id) in product.p_e_ids
