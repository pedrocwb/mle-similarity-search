import pytest


@pytest.fixture()
def reviews_data():
    return [
        {"p_e_id": "-9221563774004008904", "text": "I was able to test it"},
        {"p_e_id": "-9221563774004008904", "text": "I didn't like it"},
        {"p_e_id": "-8331563774004008904", "text": "I loved the sun protection"},
    ]


@pytest.fixture
def qw_reviews_response(reviews_data):
    return {
        "num_hits": 2,
        "hits": reviews_data,
        "elapsed_time_micros": 344481,
        "errors": [],
    }
