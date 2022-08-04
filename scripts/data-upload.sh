
mc alias set minio $MINIO_HOST $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
mc mb minio/reviews
mc cp /data/* minio/reviews