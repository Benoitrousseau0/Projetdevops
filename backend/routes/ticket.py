from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud import ticket as crud_ticket
from crud.utilisateur import get_utilisateur
from models.utilisateur import RoleEnum
from schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from utils.security import get_current_user, require_role
from utils.notifier import notifier_assignation, notifier_changement_statut

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketOut)
def creer_ticket(ticket: TicketCreate, db: Session = Depends(get_db),
                 current_user=Depends(require_role([RoleEnum.employe]))):
    return crud_ticket.create_ticket(db, ticket, current_user.id)


@router.get("/", response_model=list[TicketOut])
def lister_tickets(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role == RoleEnum.admin:
        return crud_ticket.get_all_tickets(db)
    elif current_user.role == RoleEnum.technicien:
        return crud_ticket.get_tickets_by_technicien(db, current_user.id)
    else:
        return crud_ticket.get_tickets_by_employe(db, current_user.id)


@router.get("/{ticket_id}", response_model=TicketOut)
def lire_ticket(ticket_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")
    return ticket


@router.put("/{ticket_id}", response_model=TicketOut)
def modifier_ticket(ticket_id: int, updates: TicketUpdate, db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # Employé ne peut modifier que ses tickets
    if current_user.role == RoleEnum.employe and ticket.id_employe != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")

    # Technicien : modif autorisée si assigné
    if current_user.role == RoleEnum.technicien:
        assignations = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in assignations:
            raise HTTPException(status_code=403, detail="Accès interdit")

    ticket = crud_ticket.update_ticket(db, ticket, updates)

    # Si statut changé → notifier l’employé
    if updates.statut:
        notifier_changement_statut(db, ticket)

    return ticket


@router.post("/{ticket_id}/assigner")
def assigner_techniciens(ticket_id: int, technicien_ids: list[int], db: Session = Depends(get_db),
                         current_user=Depends(require_role([RoleEnum.admin]))):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # Vérifier que tous sont des techniciens
    for tid in technicien_ids:
        user = get_utilisateur(db, tid)
        if not user or user.role != RoleEnum.technicien:
            raise HTTPException(status_code=400, detail=f"L'utilisateur {tid} n'est pas un technicien")

    crud_ticket.assign_techniciens(db, ticket_id, technicien_ids)
    notifier_assignation(db, ticket_id, technicien_ids)
    return {"message": "Techniciens assignés avec succès"}
