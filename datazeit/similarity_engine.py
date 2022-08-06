from typing import List, Tuple, Union

import pandas as pd
from SetSimilaritySearch import SearchIndex

from datazeit.logger import logger


class SimilarityEngine:
    def compute_similarity(
        self,
        p_c_id: int,
        products_df: pd.DataFrame,
        ingredients_df: pd.DataFrame,
        top: int = 5,
        similarity_threshold: float = 0.1,
        similarity_func_name: str = "jaccard",
    ) -> Union[pd.Series, None]:
        products_w_ingredients = self._process_data(products_df, ingredients_df)

        try:
            similarity_rank = self._compute_similarity_rank(
                p_c_id,
                products_w_ingredients,
                similarity_threshold,
                similarity_func_name,
                top,
            )
        except KeyError:
            logger.error(f"Could not find product {p_c_id}")
            return None

        if not similarity_rank:
            logger.error(f"There are no similar products to {p_c_id}")
            return None

        idx, values = zip(*similarity_rank)
        idx = products_w_ingredients.iloc[list(idx)].index

        similarity_rank = pd.Series(values, idx, name="p_c_id")
        return similarity_rank

    @staticmethod
    def _process_data(
        products_df: pd.DataFrame, ingredients_df: pd.DataFrame
    ) -> pd.Series:

        try:
            products_df["p_e_ids"] = products_df["p_e_ids"].apply(lambda x: eval(x))
        except TypeError:
            logger.info("p_e_ids already parsed to set.")

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

    @staticmethod
    def _compute_similarity_rank(
        p_c_id: int,
        prods_with_ingredients: pd.Series,
        similarity_threshold: float,
        similarity_func_name: str,
        top: int,
    ) -> List[Tuple[int, float]]:
        """
        Compute the distance of all products ingredients for the p_c_id to search
        and returns the top first results.
        """
        to_search = prods_with_ingredients.loc[p_c_id]

        sets = list(prods_with_ingredients)
        index = SearchIndex(
            sets,
            similarity_func_name=similarity_func_name,
            similarity_threshold=similarity_threshold,
        )
        results = index.query(to_search)
        results.sort(key=lambda k: k[1], reverse=True)

        # return top N similar ingredients
        # ignore the 1st because it's the actual product to search
        return results[1 : top + 1]
