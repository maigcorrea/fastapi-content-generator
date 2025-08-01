from pydantic import BaseModel, EmailStr

class ResendCodeDto(BaseModel):
    email: EmailStr
