from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from crud import ticket as crud_ticket
from crud.utilisateur import get_utilisateur
from models.utilisateur import RoleEnum, Utilisateur
from schemas.ticket import TicketCreate, TicketOut, TicketUpdate
from utils.security import get_current_user, require_role
from utils.notifier import notifier_assignation, notifier_changement_statut
from models.ticket import StatutEnum


router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketOut)
def creer_ticket(ticket: TicketCreate, db: Session = Depends(get_db),
                 current_user=Depends(require_role([RoleEnum.employe]))):
    created_ticket = crud_ticket.create_ticket(db, ticket, current_user.id)
    print("Ticket créé (route):", created_ticket)
    return created_ticket

@router.get("/", response_model=list[TicketOut])
def lister_tickets(
    statut: str = None,
    priorite: str = None,
    sort: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role == RoleEnum.admin:
        tickets = crud_ticket.get_all_tickets(db, statut, priorite, sort)
    elif current_user.role == RoleEnum.technicien:
        tickets = crud_ticket.get_tickets_by_technicien(db, current_user.id, statut, priorite, sort)
    else:
        tickets = crud_ticket.get_tickets_by_employe(db, current_user.id, statut, priorite, sort)

    # ✅ Transforme les tickets pour que techniciens soit une liste d'IDs
    return [
        {
            "id": t.id,
            "titre": t.titre,
            "description": t.description,
            "priorite": t.priorite,
            "statut": t.statut,
            "date_creation": t.date_creation,
            "id_employe": t.id_employe,
            "techniciens": [tt.id_technicien for tt in t.techniciens]
        }
        for t in tickets
    ]

@router.get("/{ticket_id}", response_model=TicketOut)
def lire_ticket(ticket_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # Vérification d'accès
    if current_user.role == RoleEnum.employe and ticket.id_employe != current_user.id:
        raise HTTPException(status_code=403, detail="Accès interdit")
    if current_user.role == RoleEnum.technicien:
        assignations = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in assignations:
            raise HTTPException(status_code=403, detail="Accès interdit")

    # ✅ Retourne un dict custom pour éviter l'erreur de validation
    return {
        "id": ticket.id,
        "titre": ticket.titre,
        "description": ticket.description,
        "priorite": ticket.priorite,
        "statut": ticket.statut,
        "date_creation": ticket.date_creation,
        "id_employe": ticket.id_employe,
        "techniciens": [t.id_technicien for t in ticket.techniciens]
    }

@router.put("/{ticket_id}", response_model=TicketOut)
def modifier_ticket(ticket_id: int, updates: TicketUpdate, db: Session = Depends(get_db),
                    current_user=Depends(get_current_user)):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # Vérifier si le ticket est fermé, et empêcher toute modification si c'est le cas
    if ticket.statut == StatutEnum.ferme:
        raise HTTPException(status_code=403, detail="Impossible de modifier un ticket fermé")

    # --- Employé : peut modifier uniquement ses propres tickets
    if current_user.role == RoleEnum.employe:
        if ticket.id_employe != current_user.id:
            raise HTTPException(status_code=403, detail="Accès interdit")

    # --- Technicien : peut modifier uniquement les tickets qui lui sont assignés
    elif current_user.role == RoleEnum.technicien:
        assignations = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in assignations:
            raise HTTPException(status_code=403, detail="Accès interdit")

    # --- Admin : accès autorisé
    elif current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Accès interdit")

    # --- Exécution de la mise à jour
    ticket = crud_ticket.update_ticket(db, ticket, updates)

    if updates.statut:
        notifier_changement_statut(db, ticket)

    # Retourne un dict personnalisé avec uniquement les IDs des techniciens
    return {
        "id": ticket.id,
        "titre": ticket.titre,
        "description": ticket.description,
        "priorite": ticket.priorite,
        "statut": ticket.statut,
        "date_creation": ticket.date_creation,
        "id_employe": ticket.id_employe,
        # Renvoie uniquement les IDs des techniciens
        "techniciens": [t.id_technicien for t in ticket.techniciens]  # Liste d'IDs, pas des objets
    }

@router.post("/{ticket_id}/assigner")
def assigner_techniciens(ticket_id: int, technicien_ids: list[int], db: Session = Depends(get_db),
                         current_user=Depends(require_role([RoleEnum.admin]))):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    for tid in technicien_ids:
        user = get_utilisateur(db, tid)
        if not user or user.role != RoleEnum.technicien:
            raise HTTPException(status_code=400, detail=f"L'utilisateur {tid} n'est pas un technicien")

    crud_ticket.assign_techniciens(db, ticket_id, technicien_ids)
    notifier_assignation(db, ticket_id, technicien_ids)
    return {"message": "Techniciens assignés avec succès"}

@router.delete("/{ticket_id}", response_model=dict)
def supprimer_ticket(ticket_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    # --- Employé : peut supprimer uniquement ses propres tickets ouverts
    if current_user.role == RoleEnum.employe:
        if ticket.id_employe != current_user.id or ticket.statut.lower() != "ouvert":
            raise HTTPException(
                status_code=403,
                detail="Seuls les tickets ouverts peuvent être supprimés par leur auteur"
            )

    # --- Technicien : peut supprimer uniquement les tickets qui lui sont assignés
    elif current_user.role == RoleEnum.technicien:
        assignations = [t.id_technicien for t in ticket.techniciens]
        if current_user.id not in assignations:
            raise HTTPException(
                status_code=403,
                detail="Vous ne pouvez supprimer que les tickets qui vous sont assignés"
            )

    # --- Admin : tout accès autorisé (OK)
    elif current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Accès interdit")
    print("ID utilisateur connecté:", current_user.id)
    print("ID employé du ticket:", ticket.id_employe)
    crud_ticket.delete_ticket(db, ticket_id)
    return {"message": "Ticket supprimé avec succès"}


@router.post("/{ticket_id}/desassigner")
def desassigner_technicien(ticket_id: int, technicien_id: int, db: Session = Depends(get_db),
                           current_user=Depends(require_role([RoleEnum.admin]))):
    ticket = crud_ticket.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    technicien = db.query(Utilisateur).filter(Utilisateur.id == technicien_id,
                                              Utilisateur.role == RoleEnum.technicien).first()
    if not technicien:
        raise HTTPException(status_code=404, detail="Technicien introuvable ou rôle invalide")

    # Désassigner le technicien du ticket
    crud_ticket.remove_technicien(db, ticket_id, technicien_id)

    return {"message": f"Technicien {technicien.nom} désassigné avec succès du ticket {ticket_id}"}
