from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from infrastructure.db.db_config import SessionLocal
from infrastructure.db.repositories.image_repository_impl import ImageRepositoryImpl
from infrastructure.s3.s3_client import s3_client
from config import settings
import logging

def delete_old_images():
    logging.info("🗑 Ejecutando cron para borrar imágenes eliminadas hace más de 30 días...")
    db: Session = SessionLocal()
    repo = ImageRepositoryImpl(db)
    deleted_count = 0


    limit_date = datetime.utcnow() - timedelta(days=30) # Fecha límite para eliminar imágenes antiguas
    old_images = repo.find_deleted_before(limit_date)

    for img in old_images:
        try:
            # Borrar de MinIO / S3
            s3_client.delete_object(Bucket=settings.minio_bucket, Key=img.file_name)
            # Borrar de la BD
            repo.hard_delete(img.id)
            logging.info(f"✅ Imagen {img.file_name} eliminada definitivamente")
            deleted_count += 1
        except Exception as e:
            logging.error(f"❌ Error eliminando {img.file_name}: {e}")

    db.close()

    return deleted_count