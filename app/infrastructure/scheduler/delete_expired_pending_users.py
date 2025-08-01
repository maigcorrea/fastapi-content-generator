from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.db.db_config import SessionLocal
from infrastructure.db.repositories.pending_user_repository_impl import PendingUserRepositoryImpl

def delete_expired_pending_users():
    print("🔹 Ejecutando limpieza de usuarios pendientes caducados...")
    db: Session = SessionLocal()
    try:
        repo = PendingUserRepositoryImpl(db)
        deleted_count = repo.delete_expired(datetime.utcnow())
        print(f"✅ Limpieza completada ({deleted_count} usuarios pendientes eliminados)")
    except Exception as e:
        print(f"❌ Error en limpieza de usuarios pendientes: {e}")
    finally:
        db.close()
