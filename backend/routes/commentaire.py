from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud.commentaire import create_commentaire, get_commentaires_by_ticket
from crud.ticket import get_ticket
from schemas.commentaire import CommentaireCreate, CommentaireOut
from utils.security import get_current_user
from utils.notifier import notifier_nouveau_commentaire
from models.utilisateur import RoleEnum

router = APIRouter(prefix="/commentaires", tags=["Commentaires"])

@router.post("/", response_model=CommentaireOut)
def ajouter_commentaire(commentaire: CommentaireCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ticket = get_ticket(db, commentaire.id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # Vérification des droits d'accès
    if current_user.role == RoleEnum.employe and ticket.id_employe != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    if current_user.role == RoleEnum.technicien:
        technicien_ids = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in technicien_ids:
            raise HTTPException(status_code=403, detail="Accès interdit")

    commentaire_db = create_commentaire(db, commentaire, current_user.id)
    notifier_nouveau_commentaire(db, ticket, current_user.id)
    return commentaire_db

@router.get("/ticket/{ticket_id}", response_model=list[CommentaireOut])
def lister_commentaires(ticket_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ticket = get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # Vérification des droits d'accès
    if current_user.role == RoleEnum.employe and ticket.id_employe != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    if current_user.role == RoleEnum.technicien:
        technicien_ids = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in technicien_ids:
            raise HTTPException(status_code=403, detail="Accès interdit")

    return get_commentaires_by_ticket(db, ticket_id)
