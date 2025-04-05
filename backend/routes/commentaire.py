from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud.commentaire import (
    create_commentaire, get_commentaires_by_ticket,
    delete_commentaire, update_commentaire
)
from crud.ticket import get_ticket
from schemas.commentaire import (
    CommentaireCreate, CommentaireOut, CommentaireUpdate
)
from utils.security import get_current_user
from utils.notifier import notifier_nouveau_commentaire
from models.utilisateur import RoleEnum

router = APIRouter(prefix="/commentaires", tags=["Commentaires"])


@router.post("/", response_model=CommentaireOut)
def ajouter_commentaire(commentaire: CommentaireCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ticket = get_ticket(db, commentaire.id_ticket)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

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

    if current_user.role == RoleEnum.employe and ticket.id_employe != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    if current_user.role == RoleEnum.technicien:
        technicien_ids = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in technicien_ids:
            raise HTTPException(status_code=403, detail="Accès interdit")

    return get_commentaires_by_ticket(db, ticket_id)


@router.put("/ticket/{ticket_id}/commentaires/{commentaire_id}", response_model=CommentaireOut)
def modifier_commentaire(ticket_id: int, commentaire_id: int, update: CommentaireUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    commentaires = get_commentaires_by_ticket(db, ticket_id)
    target = next((c for c in commentaires if c.id == commentaire_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Commentaire introuvable")

    if current_user.role != RoleEnum.admin and target.id_utilisateur != current_user.id:
        raise HTTPException(status_code=403, detail="Modification non autorisée")

    return update_commentaire(db, commentaire_id, update.contenu)


@router.delete("/ticket/{ticket_id}/commentaires/{commentaire_id}", response_model=dict)
def supprimer_commentaire(ticket_id: int, commentaire_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    commentaires = get_commentaires_by_ticket(db, ticket_id)
    target = next((c for c in commentaires if c.id == commentaire_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Commentaire introuvable")

    if current_user.role != RoleEnum.admin and target.id_utilisateur != current_user.id:
        raise HTTPException(status_code=403, detail="Suppression non autorisée")

    delete_commentaire(db, commentaire_id)
    return {"message": "Commentaire supprimé avec succès"}
