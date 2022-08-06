#!/bin/bash

echo "Creating conda environment"
conda create -n datazeit-mle python=3.7

echo "installing pip packages"
pip install -r requirements/requirements.txt
pip install -e datazeit/

echo "Start ETL routine"
python scripts/etl.py

echo "Running docker compose"
docker compose up -d

echo "Datazeit API initialized."
echo "Happy journey :)"
