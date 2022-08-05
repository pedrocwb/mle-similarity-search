export QW_CONFIG=/quickwit/qwdata/minio-qw-config.yaml

quickwit index create --index-config qwdata/reviews-index-config.yaml
quickwit index ingest --index reviews --input-path /data/cp_ml_eng_reviews.json
quickwit run --service searcher