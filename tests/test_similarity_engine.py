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
    expected_p_e_ids = (
        products_df.loc[products_df["p_c_id"] == product_id, "p_e_ids"]
        .apply(list)
        .iloc[0]
    )

    expected_ingredients = set(
        ingredients_df.loc[ingredients_df["p_e_id"].isin(expected_p_e_ids), "inci_name"]
    )

    actual_ingredients = set(processed_data.loc[product_id])
    assert actual_ingredients == expected_ingredients


@pytest.fixture
def prod_with_ingredients_series():
    return pd.Series(
        [
            ["A", "B", "C"],
            ["A", "B", "C", "E"],
            ["A", "B", "D"],
            ["A", "D", "G"],
            ["A", "D", "F"],
            ["H", "D", "F"],
            ["H", "L", "C"],
            ["E", "F", "H"],
            ["I", "J", "K"],
            ["B", "C", "D"],
        ],
        index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    )


def test_compute_similarity_rank(prod_with_ingredients_series):
    engine = SimilarityEngine()
    similarity_rank = engine._compute_similarity_rank(
        p_c_id=0,
        prods_with_ingredients=prod_with_ingredients_series,
        similarity_threshold=0.1,
        similarity_func_name="jaccard",
        top=5,
    )

    assert all(score >= 0.1 for ix, score in similarity_rank)
    assert len(similarity_rank) == 5
    # check if its sorted in descending order
    assert all(
        s1 >= s2 for (_, s1), (_, s2) in zip(similarity_rank, similarity_rank[1:])
    )


def test_compute_similarity(products_df, ingredients_df):
    engine = SimilarityEngine()
    res = engine.compute_similarity(
        p_c_id=1020, products_df=products_df, ingredients_df=ingredients_df
    )

    assert isinstance(res, pd.Series)
    assert res.name == "p_c_id"
    assert res.is_monotonic_decreasing

    res = engine.compute_similarity(
        p_c_id=0, products_df=products_df, ingredients_df=ingredients_df
    )
    assert not res
