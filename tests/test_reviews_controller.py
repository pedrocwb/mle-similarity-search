from unittest.mock import Mock

import pytest

from datazeit.gateways.database import ClickHouseGateway, Product
from datazeit.gateways.search_engine import QuickWitGateway
from datazeit.reviews_controller import ReviewsController


@pytest.fixture
def reviews_controller():
    return ReviewsController(
        search_engine_gtw=QuickWitGateway(), database_gtw=ClickHouseGateway()
    )


def test_get_reviews_count(reviews_controller, qw_reviews_response):
    reviews_controller.search_engine_gtw.search = Mock(return_value=qw_reviews_response)
    reviews_count = reviews_controller._get_reviews_count("Sun Protection")

    # assert first p_e_id had 2 reviews and second had 1 review
    assert list(reviews_count.values()) == [2, 1]


@pytest.fixture()
def reviews_count():
    return {
        "-9221563774004008904": 10,
        "-9214020969428800136": 3,
        "-9186876200373490841": 4,
    }


@pytest.fixture()
def products():
    prods = [
        Product(
            p_c_id=1,
            brand="brand_1",
            title="Product 1 of brand 1",
            product_type="Type 1",
            p_e_ids=[-9221563774004008904],
        ),
        Product(
            p_c_id=2,
            brand="brand_1",
            title="Product 2 of brand 1",
            product_type="Type 2",
            p_e_ids=[-9214020969428800136],
        ),
        Product(
            p_c_id=3,
            brand="brand_2",
            title="Product 1 of brand 2",
            product_type="Type 2",
            p_e_ids=[-9186876200373490841],
        ),
    ]
    return prods


def test_run_search(reviews_controller, products, reviews_count):
    reviews_controller._get_reviews_count = Mock(return_value=reviews_count)
    reviews_controller.database_gtw.get_product_by_variation = Mock(
        side_effect=products
    )

    res = reviews_controller.compute_reviews("Sun Protection")

    for rc in res["brands"]:
        if rc["brand"] == "brand_1":
            assert rc["review_count"] == 13
        if rc["brand"] == "brand_2":
            assert rc["review_count"] == 4

    for rc in res["product_type"]:
        if rc["product_type"] == "Type 1":
            assert rc["review_count"] == 10
        if rc["product_type"] == "Type 2":
            assert rc["review_count"] == 7
