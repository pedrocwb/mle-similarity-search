#!/bin/bash


echo "Start ETL routine"
python scripts/etl.py

echo "Running docker compose"
docker compose up -d

echo "Datazeit API initialized."
echo "Happy journey :)"
