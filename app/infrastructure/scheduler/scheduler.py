from apscheduler.schedulers.background import BackgroundScheduler
from infrastructure.scheduler.delete_old_images import delete_old_images
from infrastructure.scheduler.delete_expired_pending_users import delete_expired_pending_users

scheduler = BackgroundScheduler()

def start_scheduler():
    # Tarea: borrar imágenes antiguas a medianoche
    scheduler.add_job(
            #delete_old_images, "cron", hour=0, minute=0
            lambda: print(f"🗑 Imágenes eliminadas: {delete_old_images()}"),
            "cron", hour=0, minute=0
        )

    # Tarea: borrar usuarios pendientes caducados cada hora
    scheduler.add_job(
        #delete_expired_pending_users, "interval", hours=1
            lambda: print(f"🧹 Usuarios pendientes eliminados: {delete_expired_pending_users()}"),
            "interval", hours=1
        )

    if not scheduler.running:
        scheduler.start()
        print("⏱️ Scheduler started")

def stop_scheduler():
    """
    Detiene el scheduler.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Scheduler stopped")
