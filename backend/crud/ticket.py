from sqlalchemy.orm import Session
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

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def get_tickets_by_employe(db: Session, id_employe: int):
    return db.query(Ticket).filter(Ticket.id_employe == id_employe).all()

def get_tickets_by_technicien(db: Session, id_technicien: int):
    return db.query(Ticket)\
        .join(TicketTechnicien)\
        .filter(TicketTechnicien.id_technicien == id_technicien)\
        .all()

def update_ticket(db: Session, db_ticket: Ticket, updates: TicketUpdate):
    for attr, value in updates.dict(exclude_unset=True).items():
        setattr(db_ticket, attr, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def assign_techniciens(db: Session, ticket_id: int, technicien_ids: list[int]):
    # Supprimer assignations existantes
    db.query(TicketTechnicien).filter(TicketTechnicien.id_ticket == ticket_id).delete()
    # Réassigner
    for tech_id in technicien_ids:
        db.add(TicketTechnicien(id_ticket=ticket_id, id_technicien=tech_id))
    db.commit()
