from datazeit.gateways.database import ClickHouseGateway


def test_get_products():
    gtw = ClickHouseGateway()
    products = gtw.get_products(p_c_id="145")

    assert products
