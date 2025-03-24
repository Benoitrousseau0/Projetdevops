from sqlalchemy.orm import Session
from crud.notification import create_notification
from models.ticket import Ticket
from models.liaison import TicketTechnicien

def notifier_assignation(db: Session, ticket_id: int, technicien_ids: list[int]):
    for tech_id in technicien_ids:
        create_notification(db, f"Vous avez été assigné au ticket #{ticket_id}", tech_id, ticket_id)

def notifier_changement_statut(db: Session, ticket: Ticket):
    create_notification(db, f"Le ticket #{ticket.id} est maintenant {ticket.statut}", ticket.id_employe, ticket.id)

def notifier_nouveau_commentaire(db: Session, ticket: Ticket, auteur_id: int):
    techniciens = db.query(TicketTechnicien).filter(TicketTechnicien.id_ticket == ticket.id).all()
    destinataires = set([t.id_technicien for t in techniciens] + [ticket.id_employe])
    destinataires.discard(auteur_id)  # Ne pas notifier l'auteur
    for user_id in destinataires:
        create_notification(db, f"Nouveau commentaire sur le ticket #{ticket.id}", user_id, ticket.id)
