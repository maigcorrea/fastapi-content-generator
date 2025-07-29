from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MinIO / S3
    minio_endpoint: str
    minio_bucket: str
    minio_access_key: str
    minio_secret_key: str
    use_ssl: bool = False

    class Config:
        env_file = ".env"

settings = Settings()