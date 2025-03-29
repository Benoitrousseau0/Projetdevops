from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime
from typing import Optional


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

class ChangementMotDePasse(BaseModel):
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str

class MiseAJourProfil(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
