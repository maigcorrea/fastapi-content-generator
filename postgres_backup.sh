#!/bin/bash

# Configuración
CONTAINER_NAME="fastapi-content-generator-db-1"
DB_NAME="hashtagdb"
DB_USER="postgres"
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql"

# Crear carpeta de backups si no existe
mkdir -p $BACKUP_DIR

# Función de ayuda
show_help() {
  echo "Uso: $0 [backup|restore nombre_archivo.sql]"
  echo ""
  echo "  backup                Crea un nuevo backup de la base de datos"
  echo "  restore archivo.sql   Restaura un backup existente"
  exit 1
}

# Backup
backup_db() {
  echo "📦 Creando backup de la base de datos '$DB_NAME'..."
  docker exec -i $CONTAINER_NAME pg_dump -U $DB_USER -d $DB_NAME > $BACKUP_FILE
  if [ $? -eq 0 ]; then
    echo "✅ Backup creado: $BACKUP_FILE"
  else
    echo "❌ Error al crear el backup"
    exit 1
  fi
}

# Restore
restore_db() {
  FILE_TO_RESTORE="$1"
  if [ ! -f "$FILE_TO_RESTORE" ]; then
    echo "❌ El archivo '$FILE_TO_RESTORE' no existe"
    exit 1
  fi

  echo "♻️ Restaurando backup desde '$FILE_TO_RESTORE'..."
  docker exec -i $CONTAINER_NAME psql -U $DB_USER -d $DB_NAME < $FILE_TO_RESTORE
  if [ $? -eq 0 ]; then
    echo "✅ Restauración completada"
  else
    echo "❌ Error al restaurar el backup"
    exit 1
  fi
}

# Lógica principal
case "$1" in
  backup)
    backup_db
    ;;
  restore)
    if [ -z "$2" ]; then
      show_help
    fi
    restore_db "$2"
    ;;
  *)
    show_help
    ;;
esac


# CÓMO USARLO
#1️⃣ Dar permisos de ejecución:
# chmod +x postgres_backup.sh

# 2️⃣ Hacer un backup:
# ./postgres_backup.sh backup


# 3️⃣ Restaurar un backup:
# ./postgres_backup.sh restore ./backups/backup_20250731_223045.sql
