from infrastructure.s3.s3_client import s3_client
from config import settings
from fastapi import HTTPException

class GetSignedImageUrlUseCase:
    """Genera una URL firmada temporal para una imagen privada"""

    def execute(self, file_name: str, expires_in: int = 3600) -> str:
        try:
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.minio_bucket, 'Key': file_name},
                ExpiresIn=expires_in
            )
            return url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generando URL firmada: {e}")
