#!/bin/bash
set -e

clickhouse-client -n <<-EOSQL

	CREATE DATABASE IF NOT EXISTS datazeit;
	CREATE TABLE IF NOT EXISTS datazeit.ingredients (
    p_e_id String,
    ingr_id String,
    incl_name String,
	) ENGINE = MergeTree()
	PRIMARY KEY (p_e_id);

  CREATE TABLE IF NOT EXISTS datazeit.products (
    p_c_id String,
    brand String,
    title String,
    product_type String,
    p_e_ids String,
  ) ENGINE = MergeTree()
  PRIMARY KEY (p_c_id);

EOSQL

clickhouse-client \
    --query='INSERT INTO datazeit.ingredients FORMAT CSV' < /data/cp_ml_eng_ingredients.csv

clickhouse-client \
    --query='INSERT INTO datazeit.products FORMAT CSV' < /data/cp_ml_eng_products.csv
