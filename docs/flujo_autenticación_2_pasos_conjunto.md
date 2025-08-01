# Registro de usuarios con verificación por email (FastAPI + Next.js)
## 🎯 Objetivo
- Implementar un flujo completo de registro de usuarios con verificación por email:

- El usuario se registra → se crea un registro temporal y se envía un código de verificación.

- El usuario introduce el código → se activa la cuenta real en la base de datos.

- Soporte para reenviar código y limpieza de registros caducados.

## Backend (FastAPI + SQLAlchemy)

**Estructura de archivos relevantes**
```
app/
├── domain/
│   ├── entities/pending_user.py
│   └── repositories/pending_user_repository.py
├── infrastructure/
│   ├── db/
│   │   ├── models/pending_user_model.py
│   │   └── repositories/pending_user_repository_impl.py
│   ├── dto/
│   │   ├── user_pending_dto.py
│   │   └── verify_user_dto.py
│   ├── mail/email_service.py
│   ├── mappers/user_pending_mapper.py
│   └── scheduler/
│       └── delete_expired_pending_users.py
├── application/
│   └── use_cases/
│       ├── create_pending_user_use_case.py
│       └── verify_pending_user_use_case.py
└── interfaces/
    └── user_router.py

```

## Modelo de datos: tabla pending_users
Entidad de dominio (domain/entities/pending_user.py)
```py
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class PendingUser:
    id: uuid.UUID | None
    username: str
    email: str
    password_hash: str
    verification_code: str
    created_at: datetime
    expires_at: datetime

```

## Modelo SQLAlchemy (infrastructure/db/models/pending_user_model.py)
```py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.db.db_config import Base
import uuid

class PendingUser(Base):
    __tablename__ = "pending_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    verification_code = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)

```

## Servicio de envío de emails (EmailService)
📂 infrastructure/mail/email_service.py

```py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")

    def send_verification_email(self, to_email: str, code: str):
        subject = "Verifica tu cuenta"
        body = f"Tu código de verificación es: {code}"

        msg = MIMEMultipart()
        msg["From"] = self.smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)

```
Notas:

- Usamos credenciales de Gmail con contraseña de aplicación (App Password) si se tiene 2FA activo.

- También se puede usar Mailpit o Mailhog en desarrollo.

## Endpoints principales (en user_router.py)
- POST /users/register-pending: Crea un usuario pendiente y envía email.

- POST /users/verify: Verifica el código y activa el usuario.
 
- POST /users/resend-code: Reenvía un nuevo código de verificación.

```py
@router.post("/register-pending")
def register_pending_user(dto: CreatePendingUserDto, db: Session = Depends(get_db)):
    repo = PendingUserRepositoryImpl(db)
    email_service = EmailService()
    use_case = CreatePendingUserUseCase(repo, email_service)
    return use_case.execute(dto)

@router.post("/verify")
def verify_user(dto: VerifyUserDto, db: Session = Depends(get_db)):
    pending_repo = PendingUserRepositoryImpl(db)
    user_repo = UserRepositoryImpl(db)
    use_case = VerifyPendingUserUseCase(pending_repo, user_repo)
    return use_case.execute(dto)

@router.post("/resend-code")
def resend_code(dto: VerifyUserDto, db: Session = Depends(get_db)):
    pending_repo = PendingUserRepositoryImpl(db)
    email_service = EmailService()
    pending_user = pending_repo.get_by_email(dto.email)
    if not pending_user:
        raise HTTPException(status_code=404, detail="Usuario pendiente no encontrado")

    # Actualizar código y reenviar
    use_case = CreatePendingUserUseCase(pending_repo, email_service)
    use_case.resend_code(pending_user)
    return {"message": "Nuevo código enviado"}

```

## Cron job para limpiar registros caducados
📂 infrastructure/scheduler/delete_expired_pending_users.py

```py
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.db.db_config import SessionLocal
from infrastructure.db.repositories.pending_user_repository_impl import PendingUserRepositoryImpl

def delete_expired_pending_users():
    print("🔹 Limpiando usuarios pendientes caducados...")
    db: Session = SessionLocal()
    try:
        repo = PendingUserRepositoryImpl(db)
        deleted_count = repo.delete_expired(datetime.utcnow())
        print(f"✅ {deleted_count} usuarios eliminados")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

```
- Este job se registra con APScheduler en main.py y se ejecuta cada día.

# Frontend (Next.js + Axios)

## Servicios API (userService.ts)
📂 app/services/userService.ts

```ts
import axios from 'axios'

const API_URL = 'http://localhost:8000/users'

export const registerUser = async (formData: { username: string, email: string, password: string }) => {
  return (await axios.post(`${API_URL}/register-pending`, formData)).data
}

export const verifyUser = async (email: string, code: string) => {
  return (await axios.post(`${API_URL}/verify`, { email, code })).data
}

export const resendVerificationCode = async (email: string) => {
  return (await axios.post(`${API_URL}/resend-code`, { email })).data
}

```

## Formulario de registro (RegisterForm.tsx)
- Envía datos al endpoint /register-pending.

- Guarda el email en localStorage y redirige a /verify.

📂 app/components/RegisterForm.tsx

```tsx
'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { registerUser } from '@/app/services/userService'
import axios from 'axios'

export default function RegisterForm() {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' })
  const [message, setMessage] = useState<string | null>(null)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await registerUser(formData)
      localStorage.setItem('pendingEmail', formData.email)
      router.push('/verify')
    } catch (error: any) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        setMessage(`❌ ${error.response.data.detail}`)
      } else {
        setMessage('❌ Error al registrar usuario')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Inputs de username, email, password */}
      <button type="submit">Registrarse</button>
      {message && <p>{message}</p>}
    </form>
  )
}

```

## Formulario de verificación (VerifyForm.tsx)
- Obtiene el email desde localStorage.

- Introducir solo el código.

- Botón Reenviar código con cooldown de 20s.

- Botón Verificar bloqueado mientras se envía.

📂 app/components/VerifyForm.tsx
(versión completa con cooldown y spinner ya incluida en la última iteración)


## Diagrama global
```mermaid
flowchart TD

subgraph Frontend
A[RegisterForm] --> B[POST /users/register-pending]
B --> C[localStorage: pendingEmail]
C --> D[Redirigir a /verify]
D --> E[VerifyForm introduce código]
E --> F[POST /users/verify]
E -->|Click Reenviar| H[POST /users/resend-code]
end

subgraph Backend
B --> G[Crear PendingUser en BD + enviar email]
F -->|Código válido| I[Crear usuario real en tabla users]
I --> J[Eliminar registro de pending_users]
H --> K[Generar nuevo código y reenviar email]

subgraph Scheduler
L[Cron job diario]
L --> M[delete_expired_pending_users()]
M --> N[Elimina pending_users caducados]
end

F -->|Código inválido| O[Mostrar error en frontend]

```

## Comportamiento final
1. Usuario se registra → se crea un registro pending_users con caducidad.

2. Se envía un email con código.

3. Usuario es redirigido a /verify (solo introduce el código).

4. Si el código es válido:

    - Se crea el usuario en tabla users.

    - Se elimina el registro pendiente.

    - Se redirige a /login.

5. Si el código expira:

    - Puede reenviar el código.

    - Un cron job elimina registros caducados de la tabla pending_users.

