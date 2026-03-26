set -e

export MLFLOW_S3_ENDPOINT_URL="https://storage.yandexcloud.net"
export AWS_ACCESS_KEY_ID=YCAJE3Nlz8iDILW5VTYM1ihQB
export AWS_SECRET_ACCESS_KEY=YCPjvS7uwhvJpUj3bKm8X-IX4QAwBIVsvX61IL44
export AWS_BUCKET_NAME=s3-student-mle-20250626-89d46a25a6-freetrack
mlflow server \
  --backend-store-uri "postgresql://mle_20250626_89d46a25a6_freetrack:1c3b99f9a5b84339adf77b9faa2c07da@rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net:6432/playground_mle_20250626_89d46a25a6" \
  --registry-store-uri "postgresql://mle_20250626_89d46a25a6_freetrack:1c3b99f9a5b84339adf77b9faa2c07da@rc1b-uh7kdmcx67eomesf.mdb.yandexcloud.net:6432/playground_mle_20250626_89d46a25a6" \
  --default-artifact-root "s3://s3-student-mle-20250626-89d46a25a6-freetrack" \
  --no-serve-artifacts
