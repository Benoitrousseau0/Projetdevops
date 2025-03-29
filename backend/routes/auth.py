from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from crud.utilisateur import get_utilisateur_by_email
from utils.security import verify_password, create_access_token
from datetime import timedelta
from core.config import settings
from utils.ratelimit import tentative_autorisee, enregistrer_tentative


router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username

    if not tentative_autorisee(email):
        raise HTTPException(
            status_code=429,
            detail="Trop de tentatives. Réessayez plus tard."
        )

    utilisateur = get_utilisateur_by_email(db, email)
    if not utilisateur or not verify_password(form_data.password, utilisateur.mot_de_passe):
        enregistrer_tentative(email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides"
        )

    # ✅ Création du token avec expiration courte
    access_token = create_access_token(
        data={"sub": str(utilisateur.id)},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES  # généralement 15 min
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Déconnecté avec succès"}
