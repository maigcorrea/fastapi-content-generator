from pydantic import BaseModel, EmailStr

class VerifyUserDto(BaseModel):
    email: EmailStr
    code: str
