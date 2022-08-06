import pandas as pd

from datazeit.gateways.database import DatabaseGateway
from datazeit.similarity_engine import SimilarityEngine


class IngredientsController:
    def __init__(self, database_gtw: DatabaseGateway):
        self.database_gtw = database_gtw
        self.similarity_engine = SimilarityEngine()

    def find_similar_products(self, p_c_id: int, top: int = 5):
        products_df = pd.DataFrame(self.database_gtw.get_products())
        ingredients_df = pd.DataFrame(self.database_gtw.get_ingredients())

        similar_products_score = self.similarity_engine.compute_similarity(
            p_c_id=p_c_id,
            products_df=products_df,
            ingredients_df=ingredients_df,
            top=top,
        )

        similar_products = products_df[
            products_df["p_c_id"].isin(similar_products_score.index)
        ]

        # For every product present in similar_products_score, gets the information of product
        # and loops over all product`s ingredients adding them to the ingredients key
        res = {
            "similar": [
                {
                    "p_c_id": product["p_c_id"],
                    "brand": product["brand"],
                    "title": product["title"],
                    "product_type": product["product_type"],
                    "ingredients": [
                        {
                            "ingr_id": ingredient["ingr_id"],
                            "inci_name": ingredient["inci_name"],
                        }
                        for p_e_id in product["p_e_ids"]
                        for ix, ingredient in ingredients_df.loc[
                            ingredients_df["p_e_id"] == p_e_id
                        ].iterrows()
                    ],
                }
                for ix, product in similar_products.iterrows()
            ]
        }

        return res
