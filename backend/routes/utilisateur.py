from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud.utilisateur import (
    create_utilisateur, get_all_utilisateurs, get_utilisateur,
    get_utilisateur_by_email, update_mot_de_passe, update_profil
)
from schemas.utilisateur import (
    UtilisateurCreate, UtilisateurOut, ChangementMotDePasse,
    MiseAJourProfil, UtilisateurCreateInternal
)
from utils.security import get_current_user, require_role
from models.utilisateur import RoleEnum

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.post("/", response_model=UtilisateurOut)
def inscription(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    existing = get_utilisateur_by_email(db, utilisateur.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")

    utilisateur_final = UtilisateurCreateInternal(**utilisateur.dict(), role=RoleEnum.employe)
    return create_utilisateur(db, utilisateur_final)


@router.get("/moi", response_model=UtilisateurOut)
def lire_profil(current_user: UtilisateurOut = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UtilisateurOut])
def lister_utilisateurs(db: Session = Depends(get_db), current_user=Depends(require_role([RoleEnum.admin]))):
    return get_all_utilisateurs(db)


@router.put("/password", response_model=dict)
def changer_mot_de_passe(
    data: ChangementMotDePasse,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    success = update_mot_de_passe(db, current_user, data.ancien_mot_de_passe, data.nouveau_mot_de_passe)
    if not success:
        raise HTTPException(status_code=403, detail="Mot de passe actuel incorrect")
    return {"message": "Mot de passe mis à jour"}


@router.put("/moi", response_model=UtilisateurOut)
def modifier_profil(
    data: MiseAJourProfil,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return update_profil(db, current_user, data.nom, data.email)


@router.delete("/moi", response_model=dict)
def supprimer_mon_compte(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return {"message": "Compte supprimé"}


@router.delete("/{id}", response_model=dict)
def supprimer_utilisateur(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([RoleEnum.admin]))
):
    utilisateur = get_utilisateur(db, id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(utilisateur)
    db.commit()
    return {"message": "Utilisateur supprimé avec succès"}
