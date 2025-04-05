from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import datetime
from typing import Optional


# --- Enums ---
class RoleEnum(str, Enum):
    employe = "employe"
    technicien = "technicien"
    admin = "admin"


# --- Base ---
class UtilisateurBase(BaseModel):
    nom: str
    email: EmailStr
    role: RoleEnum


# --- Create ---
class UtilisateurCreate(BaseModel):
    nom: str
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=6, max_length=128)

class UtilisateurCreateInternal(UtilisateurCreate):
    role: RoleEnum

# --- Update ---
class MiseAJourProfil(BaseModel):
    nom: Optional[str] = None
    email: Optional[EmailStr] = None

class ChangementMotDePasse(BaseModel):
    ancien_mot_de_passe: str
    nouveau_mot_de_passe: str = Field(..., min_length=8)


# --- Out ---
class UtilisateurOut(UtilisateurBase):
    id: int
    date_inscription: datetime

    class Config:
        orm_mode = True


# --- Short (pour inclusion dans d'autres objets) ---
class UtilisateurShort(BaseModel):
    id: int
    nom: str

    class Config:
        orm_mode = True


# --- InDB (optionnel, usage interne) ---
class UtilisateurInDB(UtilisateurOut):
    hashed_password: str

    class Config:
        orm_mode = True


# --- Login ---
class UtilisateurLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str

class UpdateUserRoleRequest(BaseModel):
    new_role: RoleEnum