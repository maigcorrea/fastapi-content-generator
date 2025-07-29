# Integración de MinIO con FastAPI (compatible con AWS S3)
## 1. ¿Qué hemos hecho?
- Hemos integrado MinIO como almacenamiento de objetos en un proyecto FastAPI.

- Las imágenes se suben a MinIO en lugar de guardarse en local.

- La URL de cada imagen se registra en la base de datos para poder listarla y servirla.

- Toda la lógica de negocio se centralizó en el caso de uso UploadImageUseCase, manteniendo limpio el router.

- La integración está pensada para ser 100% compatible con AWS S3: el día que queramos migrar, solo debemos cambiar variables de entorno.



## 2. Herramientas utilizadas
- MinIO: servidor de almacenamiento de objetos auto-hosteado compatible con la API de Amazon S3.

- boto3: cliente oficial de AWS S3 en Python, también compatible con MinIO.

- FastAPI: framework backend donde se integró el flujo.

- Docker & Docker Compose: para levantar contenedores de MinIO, FastAPI y Postgres.

- pydantic-settings: para gestionar las variables de entorno en el proyecto.


## 3. Configuración en docker-compose.yml
Añadimos un servicio minio:
```
minio:
  image: minio/minio
  container_name: minio
  ports:
    - "9000:9000"   # API S3
    - "9001:9001"   # Consola web
  environment:
    MINIO_ROOT_USER: minioadmin
    MINIO_ROOT_PASSWORD: minioadmin
  command: server /data --console-address ":9001"
  volumes:
    - ./data/minio:/data
```
- Consola web: http://localhost:9001

- API interna (FastAPI): http://minio:9000



## 4. Variables de entorno (.env)
```
# Base de datos
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=hashtagdb

# MinIO / S3
MINIO_ENDPOINT=http://minio:9000
MINIO_BUCKET=images
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
USE_SSL=false
```

- Cuando migremos a AWS S3 solo debemos cambiar estas variables (quitar el MINIO_ENDPOINT y poner las credenciales de AWS).


## 5. Cliente boto3 compatible MinIO / AWS
Creamos infrastructure/s3/s3_client.py:
```python
import boto3
import os

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY"),
    endpoint_url=os.getenv("MINIO_ENDPOINT") or None,  # None en AWS
    region_name="us-east-1",
    use_ssl=os.getenv("USE_SSL", "false").lower() == "true"
)
```

## 6. Caso de uso UploadImageUseCase
Encapsula la subida a MinIO y el registro en BD:

```python
class UploadImageUseCase:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository

    def execute(self, dto: ImageCreateDTO, file_obj) -> Image:
        try:
            s3_client.upload_fileobj(file_obj, settings.minio_bucket, dto.file_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error subiendo a MinIO/S3: {e}")

        dto.url = f"{settings.minio_endpoint}/{settings.minio_bucket}/{dto.file_name}"

        image_entity = ImageMapper.from_create_dto(dto)
        image_entity.id = uuid.uuid4()
        image_entity.created_at = datetime.utcnow()

        return self.image_repository.save(image_entity)
```
## 7. Router simplificado
El router ahora solo delega al caso de uso:
```python
@router.post("/upload", response_model=ImageResponseDTO)
def upload_image(file: UploadFile, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    file_extension = os.path.splitext(file.filename)[1]
    new_file_name = f"{uuid4()}{file_extension}"

    dto = ImageCreateDTO(file_name=new_file_name, url="", user_id=current_user.id)
    use_case = UploadImageUseCase(ImageRepositoryImpl(db))
    image_entity = use_case.execute(dto, file.file)

    return ImageMapper.to_response_dto(image_entity)
```

## 8. ¿Cómo migrar a AWS S3?
Cuando quieras usar AWS S3:
1. Crea un bucket en AWS S3.


2. Pon en el .env:
```
MINIO_ENDPOINT=
MINIO_BUCKET=<tu-bucket>
MINIO_ACCESS_KEY=<AWS_ACCESS_KEY_ID>
MINIO_SECRET_KEY=<AWS_SECRET_ACCESS_KEY>
USE_SSL=true
```
- No necesitas tocar el código: boto3 detectará automáticamente el endpoint de AWS.



## 9. Próximos pasos
- Buckets privados + URLs firmadas:
    - Generar URLs temporales (ej. 1 hora) en lugar de guardar las imágenes públicas.
[Pincha aquí para ver la documentación de buckets privados](https://github.com/maigcorrea/fastapi-content-generator/blob/main/docs/gestión_img_privadas_url_firmadas.md)

