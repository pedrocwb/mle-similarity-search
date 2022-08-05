import sys
import csv
import json
import numpy as np
from datazeit.config import ROOT_DIR

#


def convert_reviews_data_to_json(
    csv_path: str = f"{ROOT_DIR}/data/cp_ml_eng_reviews.csv",
):
    save_path = f"{csv_path.split('.csv')[0]}.json"

    with open(save_path, "w+") as json_fp:
        with open(csv_path) as csv_fp:
            for entry in csv.DictReader(csv_fp.readlines()):
                json_entry = json.dumps(
                    {"p_e_id": entry["p_e_id"], "text": entry["text"]}
                )
                json_fp.write(json_entry)
                json_fp.write("\n")


def convert_products_to_json(csv_path: str = f"{ROOT_DIR}/data/cp_ml_eng_products.csv"):
    save_path = f"{csv_path.split('.csv')[0]}.json"

    with open(save_path, "w+") as json_fp:
        with open(csv_path) as csv_fp:
            for entry in csv.DictReader(csv_fp.readlines()):
                json_entry = json.dumps(
                    {
                        "p_c_id": int(entry["p_c_id"]),
                        "brand": entry["brand"],
                        "title": entry["title"],
                        "product_type": entry["product_type"],
                        "p_e_ids": [
                            int(i) for i in eval(entry["p_e_ids"])
                        ],  # transform to list of p_e_ids
                    }
                )
                json_fp.write(json_entry)
                json_fp.write("\n")


def convert_ingredients_to_json(
    csv_path: str = f"{ROOT_DIR}/data/cp_ml_eng_ingredients.csv",
):
    save_path = f"{csv_path.split('.csv')[0]}.json"

    with open(save_path, "w+") as json_fp:
        with open(csv_path) as csv_fp:
            for entry in csv.DictReader(csv_fp.readlines()):
                json_entry = json.dumps(
                    {
                        "p_e_id": int(entry["p_e_id"]),
                        "ingr_id": int(entry["ingr_id"]),
                        "inci_name": entry["inci_name"],
                    }
                )
                json_fp.write(json_entry)
                json_fp.write("\n")


convert_reviews_data_to_json()
