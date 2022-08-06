import os
import csv
import json
import logging
import sys

import requests

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("DatazeitETL")


REVIEWS_CSV_URL = (
    "https://s3.eu-central-1.wasabisys.com/dz-shared/wilhelm/cp_ml_eng_reviews.csv"
)
PRODUCTS_CSV_URL = (
    "https://s3.eu-central-1.wasabisys.com/dz-shared/wilhelm/cp_ml_eng_products.csv"
)
INGREDIENTS_CSV_URL = (
    "https://s3.eu-central-1.wasabisys.com/dz-shared/wilhelm/cp_ml_eng_ingredients.csv"
)


class DatazeitETL:
    def __init__(self):
        self._session = requests.session()

    def run(self):
        logger.info("Running Datazeit ETL.")

        os.makedirs("../data", exist_ok=True)

        self.download_reviews_data()
        self.download_products_data()
        self.download_ingredients_data()

        self._session.close()
        logger.info("Finished running Datazeit ETL.")

    def _download_file(self, url: str):
        download = self._session.get(url)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        return cr

    def download_reviews_data(self):
        logger.info("Downloading and converting Reviews data")
        save_path = f"../data/{REVIEWS_CSV_URL.split('/')[-1].replace('.csv', '.json')}"
        cr = self._download_file(REVIEWS_CSV_URL)

        with open(save_path, "w+") as json_fp:
            for p_e_id, text in list(cr)[1:]:
                json_entry = json.dumps({"p_e_id": p_e_id, "text": text})
                json_fp.write(json_entry)
                json_fp.write("\n")

        logger.info(f"Finished downloading reviews data. Saved to {save_path}")

    def download_products_data(self):
        logger.info("Downloading and converting Products data")
        save_path = (
            f"../data/{PRODUCTS_CSV_URL.split('/')[-1].replace('.csv', '.json')}"
        )
        cr = self._download_file(PRODUCTS_CSV_URL)

        with open(save_path, "w+") as json_fp:
            for p_c_id, brand, title, product_type, p_e_ids in list(cr)[1:]:
                json_entry = json.dumps(
                    {
                        "p_c_id": int(p_c_id),
                        "brand": brand,
                        "title": title,
                        "product_type": product_type,
                        "p_e_ids": [
                            int(i) for i in eval(p_e_ids)
                        ],  # transform to list of p_e_ids
                    }
                )
                json_fp.write(json_entry)
                json_fp.write("\n")

        logger.info(f"Finished downloading products data. Saved to {save_path}")

    def download_ingredients_data(self):
        logger.info("Downloading and converting Ingredients data")
        save_path = (
            f"../data/{INGREDIENTS_CSV_URL.split('/')[-1].replace('.csv', '.json')}"
        )
        cr = self._download_file(INGREDIENTS_CSV_URL)

        with open(save_path, "w+") as json_fp:
            for p_e_id, ingr_id, inci_name in list(cr)[1:]:
                json_entry = json.dumps(
                    {
                        "p_e_id": int(p_e_id),
                        "ingr_id": int(ingr_id),
                        "inci_name": inci_name,
                    }
                )
                json_fp.write(json_entry)
                json_fp.write("\n")

        logger.info(f"Finished downloading Ingredients data. Saved to {save_path}")


if __name__ == "__main__":
    etl = DatazeitETL()
    etl.run()
