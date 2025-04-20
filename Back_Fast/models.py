\
# filepath: c:\\Users\\josue\\Desktop\\Escuela_online\\Back_Fast\\models.py
from pydantic import BaseModel, EmailStr

# --- Modelos Pydantic para Validación ---
class UserBase(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    telefono: str | None = None # Hacer teléfono opcional

class UserCreate(UserBase):
    password: str

# Modelo para el login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
# --- Fin Modelos Pydantic ---
