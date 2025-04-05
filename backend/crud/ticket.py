from sqlalchemy.orm import Session
from sqlalchemy import func
from models.ticket import Ticket, StatutEnum
from models.liaison import TicketTechnicien
from schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(db: Session, ticket: TicketCreate, id_employe: int):
    db_ticket = Ticket(**ticket.dict(), id_employe=id_employe)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    print("📦 Ticket en base (CRUD):", {
        "id": db_ticket.id,
        "titre": db_ticket.titre,
        "statut": db_ticket.statut,
        "priorite": db_ticket.priorite
    })
    return db_ticket


def get_ticket(db: Session, ticket_id: int):
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def get_all_tickets(db: Session, statut=None, priorite=None, sort=None):
    query = db.query(Ticket)
    if statut:
        query = query.filter(Ticket.statut == statut)
    if priorite:
        query = query.filter(Ticket.priorite == priorite)
    if sort == "date_asc":
        query = query.order_by(Ticket.date_creation.asc())
    elif sort == "date_desc":
        query = query.order_by(Ticket.date_creation.desc())
    return query.all()


def get_tickets_by_employe(db: Session, id_employe: int, statut=None, priorite=None, sort=None):
    query = db.query(Ticket).filter(Ticket.id_employe == id_employe)
    if statut:
        query = query.filter(Ticket.statut == statut)
    if priorite:
        query = query.filter(Ticket.priorite == priorite)
    if sort == "date_asc":
        query = query.order_by(Ticket.date_creation.asc())
    elif sort == "date_desc":
        query = query.order_by(Ticket.date_creation.desc())
    return query.all()


def get_tickets_by_technicien(db: Session, id_technicien: int, statut=None, priorite=None, sort=None):
    query = db.query(Ticket).join(TicketTechnicien).filter(TicketTechnicien.id_technicien == id_technicien)
    if statut:
        query = query.filter(Ticket.statut == statut)
    if priorite:
        query = query.filter(Ticket.priorite == priorite)
    if sort == "date_asc":
        query = query.order_by(Ticket.date_creation.asc())
    elif sort == "date_desc":
        query = query.order_by(Ticket.date_creation.desc())
    return query.all()


def update_ticket(db: Session, db_ticket: Ticket, updates: TicketUpdate):
    for attr, value in updates.dict(exclude_unset=True).items():
        setattr(db_ticket, attr, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def assign_techniciens(db: Session, ticket_id: int, technicien_ids: list[int]):
    db.query(TicketTechnicien).filter(TicketTechnicien.id_ticket == ticket_id).delete()
    for tech_id in technicien_ids:
        db.add(TicketTechnicien(id_ticket=ticket_id, id_technicien=tech_id))
    db.commit()


def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket:
        db.delete(ticket)
        db.commit()

def remove_technicien(db: Session, ticket_id: int, technicien_id: int):
    ticket_technicien = db.query(TicketTechnicien).filter(TicketTechnicien.id_ticket == ticket_id, TicketTechnicien.id_technicien == technicien_id).first()
    if ticket_technicien:
        db.delete(ticket_technicien)
        db.commit()

def get_tickets_by_status(db: Session, status: StatutEnum):
    """Récupère les tickets selon le statut (ouvert, résolu, etc.)."""
    tickets = db.query(Ticket).filter(Ticket.statut == status).all()
    return tickets


def get_avg_resolution_time_by_technician(db: Session):
    # Calcul du temps moyen de résolution par technicien
    result = db.query(
        TicketTechnicien.id_technicien,  # Utilisation de la bonne colonne pour l'ID du technicien
        func.avg(Ticket.date_mise_a_jour - Ticket.date_creation).label('avg_resolution_time')
    ).join(
        Ticket, Ticket.id == TicketTechnicien.id_ticket  # Jointure correcte entre Ticket et TicketTechnicien
    ).group_by(TicketTechnicien.id_technicien).all()

    # Transformation du résultat en une liste de dictionnaires
    avg_resolution_time_by_technician = [
        {"technicien_id": technicien_id, "avg_resolution_time": avg_resolution_time}
        for technicien_id, avg_resolution_time in result
    ]

    return avg_resolution_time_by_technician

def get_critical_tickets(db: Session):
    """Récupère les tickets critiques basés sur leur priorité."""
    critical_tickets = db.query(Ticket).filter(Ticket.priorite == 'critique').all()
    return critical_tickets