from datazeit.gateways.database import DatabaseGateway


class IngredientsController:
    def __init__(self, database_gtw: DatabaseGateway):
        self.database_gtw = database_gtw

    def find_similar_products(self, p_c_id: str):
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
