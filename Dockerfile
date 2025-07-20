# Dockerfile para la aplicación FastAPI
# Utiliza una imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requisitos de forma explícita al destino
COPY requirements.txt /app/requirements.txt

# Instala dependencias desde la ruta absoluta
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo el contenido de tu carpeta app al contenedor
COPY ./app /app/app

# Comando de inicio de la app (ajustado a la nueva ruta)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
