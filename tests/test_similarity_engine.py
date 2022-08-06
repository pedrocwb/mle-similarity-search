import pandas as pd
import pytest

from datazeit.similarity_engine import SimilarityEngine


@pytest.fixture
def products_df():
    return pd.read_csv("assets/products.csv")


@pytest.fixture
def ingredients_df():
    return pd.read_csv(
        "assets/ingredients.csv",
    )


def test_process_data(products_df, ingredients_df):
    engine = SimilarityEngine()
    processed_data = engine._process_data(
        products_df=products_df, ingredients_df=ingredients_df
    )

    product_id = processed_data.index[0]
    expected_p_e_ids = products_df.loc[products_df["p_c_id"] == product_id, "p_e_ids"]
    expected_ingredients = set(
        ingredients_df.loc[ingredients_df["p_e_id"].isin(expected_p_e_ids), "inci_name"]
    )

    actual_ingredients = set(processed_data.loc[product_id])
    assert actual_ingredients == expected_ingredients
