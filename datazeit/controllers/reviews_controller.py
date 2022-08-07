from typing import Dict

from datazeit.gateways.database import DatabaseGateway
from datazeit.gateways.search_engine import SearchEngineGateway
from datazeit.logger import logger


class ReviewCountDict(dict):
    def __init__(self, *args, **kwargs):
        self.hits = {}
        super(ReviewCountDict, self).__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key not in self.keys():
            self.__setitem__(key, 0)
        return super(ReviewCountDict, self).__getitem__(key)


class ReviewsController:
    _index_: str = "reviews"

    def __init__(
        self, search_engine_gtw: SearchEngineGateway, database_gtw: DatabaseGateway
    ):
        self.search_engine_gtw = search_engine_gtw
        self.database_gtw = database_gtw

    def compute_reviews(self, keywords: str):
        logger.info(
            f"Computing amount of reviews per product/ingredient which contains the keywords {keywords}"
        )

        review_count_dict = self._get_reviews_count(keywords)
        products = [
            (p_e_id, self.database_gtw.get_product_by_variation(p_e_id))
            for p_e_id in review_count_dict.keys()
        ]

        brand_count, prod_count = {}, {}
        for p_e_id, product in products:
            review_count = review_count_dict[p_e_id]

            prev_brand_count = brand_count.get(product.brand, 0)
            brand_count[product.brand] = review_count + prev_brand_count

            prev_prod_count = prod_count.get(product.product_type, 0)
            prod_count[product.product_type] = review_count + prev_prod_count

        res = {
            "brands": [{"brand": k, "review_count": v} for k, v in brand_count.items()],
            "product_type": [
                {"product_type": k, "review_count": v} for k, v in prod_count.items()
            ],
        }

        logger.info(f"Reviews: \n {res}")
        return res

    def _get_reviews_count(self, keywords: str) -> Dict[str, int]:
        reviews = self.search_engine_gtw.search(self._index_, keywords)

        hit_count = ReviewCountDict()
        for review in reviews["hits"]:
            hit_count[review["p_e_id"]] += 1

        return hit_count
