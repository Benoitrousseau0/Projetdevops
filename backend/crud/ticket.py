from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.ticket import Ticket
from models.liaison import TicketTechnicien
from schemas.ticket import TicketCreate, TicketUpdate


def create_ticket(db: Session, ticket: TicketCreate, id_employe: int):
    db_ticket = Ticket(**ticket.dict(), id_employe=id_employe)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
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
