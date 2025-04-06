# routes/test_util.py

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from utils.security import hash_password, create_access_token
from models.utilisateur import Utilisateur
from schemas.utilisateur import RoleEnum

router = APIRouter(prefix="/tests", tags=["Tests"])

@router.post("/create-admin")
def test_create_admin(db: Session = Depends(get_db)):
    utilisateur = Utilisateur(
        nom="AdminTest",
        email=f"admin_{uuid4().hex[:6]}@mail.com",
        mot_de_passe=hash_password("admin123"),
        role=RoleEnum.admin
    )
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)

    token = create_access_token({"sub": str(utilisateur.id)})
    return {"id": utilisateur.id, "token": token}



@router.post("/create-technicien")
def test_create_technicien(db: Session = Depends(get_db)):
    utilisateur = Utilisateur(
        nom="TechTest",
        email=f"tech_{uuid4().hex[:6]}@mail.com",
        mot_de_passe=hash_password("tech123"),
        role=RoleEnum.technicien
    )
    db.add(utilisateur)
    db.commit()
    db.refresh(utilisateur)

    token = create_access_token({"sub": str(utilisateur.id)})
    return {"id": utilisateur.id, "token": token}
