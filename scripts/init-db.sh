#!/bin/bash
set -e

clickhouse-client -n <<-EOSQL

	CREATE DATABASE IF NOT EXISTS datazeit;
	CREATE TABLE IF NOT EXISTS datazeit.ingredients (
    p_e_id Int64,
    ingr_id Int64,
    incl_name String,
	) ENGINE = MergeTree()
	PRIMARY KEY (p_e_id);

  CREATE TABLE IF NOT EXISTS datazeit.products (
    p_c_id Int64,
    brand String,
    title String,
    product_type String,
    p_e_ids Array(Int64),
  ) ENGINE = MergeTree()
  PRIMARY KEY (p_c_id);

EOSQL

clickhouse-client \
    --query='INSERT INTO datazeit.ingredients FORMAT JSONEachRow' < /data/cp_ml_eng_ingredients.json

clickhouse-client \
    --query='INSERT INTO datazeit.products FORMAT JSONEachRow' < /data/cp_ml_eng_products.json
