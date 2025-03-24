from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud.utilisateur import create_utilisateur, get_all_utilisateurs, get_utilisateur, get_utilisateur_by_email
from schemas.utilisateur import UtilisateurCreate, UtilisateurOut
from utils.security import get_current_user, require_role
from models.utilisateur import RoleEnum

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

@router.post("/", response_model=UtilisateurOut)
def inscription(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    existing = get_utilisateur_by_email(db, utilisateur.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    return create_utilisateur(db, utilisateur)

@router.get("/moi", response_model=UtilisateurOut)
def lire_profil(current_user: UtilisateurOut = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=list[UtilisateurOut])
def lister_utilisateurs(db: Session = Depends(get_db), current_user = Depends(require_role([RoleEnum.admin]))):
    return get_all_utilisateurs(db)
