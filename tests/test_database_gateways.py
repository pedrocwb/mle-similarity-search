from datazeit.gateways.database import ClickHouseGateway, Product


def test_get_products():
    gtw = ClickHouseGateway()
    product = gtw.get_product_by_variation(p_e_id="5744705805828983682")

    assert isinstance(product, Product)
