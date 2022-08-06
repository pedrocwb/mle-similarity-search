import pandas as pd


class SimilarityEngine:
    def compute_similarity(
        self,
        p_c_id: str,
        products_df: pd.DataFrame,
        ingredients_df: pd.DataFrame,
        similarity_threshold: float = 0.1,
        top: int = 5,
    ):
        ...

    @staticmethod
    def _process_data(
        products_df: pd.DataFrame, ingredients_df: pd.DataFrame
    ) -> pd.Series:
        # create multiple rows  for products with multiple ingredients p_e_id
        products = products_df.explode("p_e_ids")

        # turn ingredients into list grouped by p_e_id
        list_ingredients = ingredients_df.groupby("p_e_id")["inci_name"].apply(list)

        # merge product with their ingredients and
        # drop products which ingredients were not found and
        prods_w_ingredients = products.merge(
            list_ingredients, left_on="p_e_ids", right_on="p_e_id", how="left"
        ).dropna()

        # group products within a same row with ingredients name as list
        # incl_name becomes a list of lists
        prods_w_ingredients = prods_w_ingredients.groupby("p_c_id")["inci_name"].apply(
            list
        )

        # remove duplicate ingredients
        prods_w_ingredients = prods_w_ingredients.apply(
            lambda x: list(set([c for li in x for c in li]))
        )

        return prods_w_ingredients
