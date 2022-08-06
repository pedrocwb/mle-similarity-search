from unittest.mock import MagicMock, patch

import pytest

from datazeit.api import app
from fastapi.testclient import TestClient


@pytest.fixture
def review_count_by_product_and_brand():
    return {
        "brands": [
            {
                "brand": "brand_1",
                "review_count": 10,
            }
        ],
        "product_type": [{"product_type": "Type 1", "review_count": 5}],
    }


@pytest.fixture
def similar_products_on_ingredients():
    return {
        "similar": [
            {
                "p_c_id": "pc1234",
                "brand": "b123",
                "title": "t123",
                "product_type": "p123",
                "ingredients": [{"ing_id": 1234, "inci_name": "in1234"}],
            },
        ]
    }


@patch("datazeit.api.ReviewsController")
def test_compute_reviews_by_brand_and_product(mock, review_count_by_product_and_brand):
    mocked_review_controller = mock.return_value
    mocked_review_controller.compute_reviews = MagicMock(
        return_value=review_count_by_product_and_brand
    )

    with TestClient(app) as client:
        response = client.post("/api/v1/reviews", json={"text": "sun protection"})
        assert response.status_code == 200
        assert response.json() == review_count_by_product_and_brand


@patch("datazeit.api.IngredientsController")
def test_compute_similar_products(mock, similar_products_on_ingredients):
    mocked_ingredients_controller = mock.return_value
    mocked_ingredients_controller.find_similar_products = MagicMock(
        return_value=similar_products_on_ingredients
    )

    with TestClient(app) as client:
        response = client.post("/api/v1/ingredients", json={"p_c_id": "415"})
        assert response.status_code == 200
        assert response.json() == similar_products_on_ingredients
