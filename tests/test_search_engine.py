from unittest.mock import Mock
from datazeit.gateways.search_engine import QuickWitGateway


def test_search(qw_reviews_response):
    gtw = QuickWitGateway()
    gtw._make_request = Mock(return_value=qw_reviews_response)
    data = gtw.search(index="reviews", search_term="sun protection")

    gtw._make_request.assert_called_with("sun+AND+protection", "reviews")
