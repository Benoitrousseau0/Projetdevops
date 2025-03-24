from sqlalchemy.orm import Session
from models.notification import Notification
from datetime import datetime

def create_notification(db: Session, message: str, id_utilisateur: int, id_ticket: int = None):
    notif = Notification(
        message=message,
        date_envoi=datetime.utcnow(),
        id_utilisateur=id_utilisateur,
        id_ticket=id_ticket
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def get_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.id_utilisateur == user_id).order_by(Notification.date_envoi.desc()).all()

def mark_as_read(db: Session, notif_id: int, user_id: int):
    notif = db.query(Notification).filter(Notification.id == notif_id, Notification.id_utilisateur == user_id).first()
    if notif:
        notif.lu = True
        db.commit()
        db.refresh(notif)
    return notif

def mark_all_as_read(db: Session, user_id: int):
    db.query(Notification).filter(Notification.id_utilisateur == user_id, Notification.lu == False).update({Notification.lu: True})
    db.commit()
