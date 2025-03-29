from sqlalchemy.orm import Session
from models.utilisateur import Utilisateur
from schemas.utilisateur import UtilisateurCreate
from utils.security import hash_password, verify_password
from typing import Optional

def get_utilisateur_by_email(db: Session, email: str):
    return db.query(Utilisateur).filter(Utilisateur.email == email).first()

def get_utilisateur(db: Session, user_id: int):
    return db.query(Utilisateur).filter(Utilisateur.id == user_id).first()

def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    hashed_pw = hash_password(utilisateur.mot_de_passe)
    db_user = Utilisateur(
        nom=utilisateur.nom,
        email=utilisateur.email,
        mot_de_passe=hashed_pw,
        role=utilisateur.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_utilisateurs(db: Session):
    return db.query(Utilisateur).all()


def update_mot_de_passe(db: Session, utilisateur: Utilisateur, ancien: str, nouveau: str):
    if not verify_password(ancien, utilisateur.mot_de_passe):
        return False
    utilisateur.mot_de_passe = hash_password(nouveau)
    db.commit()
    return True

def update_profil(db: Session, utilisateur: Utilisateur, nom: Optional[str], email: Optional[str]):
    if nom:
        utilisateur.nom = nom
    if email:
        utilisateur.email = email
    db.commit()
    db.refresh(utilisateur)
    return utilisateur
