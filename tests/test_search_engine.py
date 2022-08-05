from unittest.mock import Mock

import pytest

from datazeit.gateways.search_engine import QuickWitGateway


@pytest.fixture()
def reviews_data():
    return [
        {"p_e_id": "-9221563774004008904", "text": "I was able to test"},
        {"p_e_id": "-8331563774004008904", "text": "I loved the sun screen"},
    ]


@pytest.fixture
def qw_reviews_response(reviews_data):
    return {
        "num_hits": 2,
        "hits": reviews_data,
        "elapsed_time_micros": 344481,
        "errors": [],
    }


def test_search(qw_reviews_response):
    gtw = QuickWitGateway()
    gtw._make_request = Mock(return_value=qw_reviews_response)
    data = gtw.search(index="reviews", search_term="sun protection")

    gtw._make_request.assert_called_with("sun+AND+protection", "reviews")
