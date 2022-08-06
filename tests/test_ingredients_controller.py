from unittest.mock import MagicMock
from datazeit.gateways.database import ClickHouseGateway
from datazeit.ingredients_controller import IngredientsController


def test_find_similar_products(products_df, ingredients_df):
    controller = IngredientsController(database_gtw=ClickHouseGateway())
    controller.database_gtw.get_products = MagicMock(return_value=products_df.to_dict())
    controller.database_gtw.get_ingredients = MagicMock(
        return_value=ingredients_df.to_dict()
    )

    res = controller.find_similar_products(p_c_id=1020, top=5)

    assert len(res["similar"]) == 5
    assert all(len(prod["ingredients"]) > 0 for prod in res["similar"])
