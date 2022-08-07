import os
import csv
import json
import logging
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    import pip

    pip.main(["install", requests])


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("DatazeitETL")

ROOT_DIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)

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
        self._save_dir = f"{ROOT_DIR}/data"

    def run(self):
        logger.info("Running Datazeit ETL.")
        logger.info(f"Data will be saved to {self._save_dir}")

        os.makedirs(self._save_dir, exist_ok=True)

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

    @staticmethod
    def _check_file_exists(url):
        if os.path.exists(url):
            logger.info("File already exist. The ETL won't download it again.")
            return True
        return False

    def download_reviews_data(self):
        logger.info("Downloading and converting Reviews data")
        save_path = f"{self._save_dir}/{REVIEWS_CSV_URL.split('/')[-1].replace('.csv', '.json')}"

        if not self._check_file_exists(save_path):
            cr = self._download_file(REVIEWS_CSV_URL)

            with open(save_path, "w+") as json_fp:
                for p_e_id, text in list(cr)[1:]:
                    json_entry = json.dumps({"p_e_id": p_e_id, "text": text})
                    json_fp.write(json_entry)
                    json_fp.write("\n")

            logger.info(f"Finished downloading reviews data. Saved to {save_path}")

    def download_products_data(self):
        logger.info("Downloading and converting Products data")
        save_path = f"{self._save_dir}/{PRODUCTS_CSV_URL.split('/')[-1].replace('.csv', '.json')}"
        cr = self._download_file(PRODUCTS_CSV_URL)
        if not self._check_file_exists(save_path):
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
        save_path = f"{self._save_dir}/{INGREDIENTS_CSV_URL.split('/')[-1].replace('.csv', '.json')}"
        if not self._check_file_exists(save_path):
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
