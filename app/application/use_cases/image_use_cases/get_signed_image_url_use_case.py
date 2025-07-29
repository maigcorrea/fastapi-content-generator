from infrastructure.s3.s3_client import s3_client
from config import settings
from fastapi import HTTPException
import os

class GetSignedImageUrlUseCase:
    """Genera una URL firmada temporal para una imagen privada"""

    def execute(self, file_name: str, expires_in: int = 3600) -> str:
        try:
            # Generar la URL firmada usando endpoint que tenga boto3 (MinIO/S3)
            url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.minio_bucket, 'Key': file_name},
                ExpiresIn=expires_in
            )
            
            # Reemplazar el host interno (minio:9000) por el host público (localhost:9000) para acceso desde el navegador
            # Si estamos en MinIO (local o servidor) sustituimos el host interno por el público
            # Si la URL generada contiene amazonaws.com → estamos en AWS, la devolvemos tal cual.
            # Si no contiene amazonaws.com → estamos en MinIO y sustituimos el host interno por el público (MINIO_PUBLIC_HOST).
            if settings.minio_endpoint and "amazonaws.com" not in url:
                public_host = os.getenv("MINIO_PUBLIC_HOST", "http://localhost:9000")
                internal_host = settings.minio_endpoint.replace("http://", "").replace("https://", "")

                return url.replace(internal_host, public_host.replace("http://", "").replace("https://", ""))

            # Si es AWS S3 no hacemos nada, ya es accesible públicamente
            return url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generando URL firmada: {e}")
