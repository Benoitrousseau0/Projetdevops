from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

class RoleEnum(str, Enum):
    employe = "employe"
    technicien = "technicien"
    admin = "admin"

class UtilisateurBase(BaseModel):
    nom: str
    email: EmailStr
    role: RoleEnum

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class UtilisateurOut(UtilisateurBase):
    id: int
    date_inscription: datetime

    class Config:
        orm_mode = True

class UtilisateurLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str
