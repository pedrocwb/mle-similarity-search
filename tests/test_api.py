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
