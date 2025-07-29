import boto3
import os

# Configuración del cliente S3 usando las variables de entorno 
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    endpoint_url=os.getenv("MINIO_ENDPOINT"),
    region_name="us-east-1",  # o la región que uses en AWS (no afecta en MinIO)
    use_ssl=os.getenv("USE_SSL", "false").lower() == "true"
)
