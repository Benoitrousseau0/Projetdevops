from sqlalchemy.orm import Session
from models.commentaire import Commentaire
from schemas.commentaire import CommentaireCreate

def create_commentaire(db: Session, commentaire: CommentaireCreate, user_id: int):
    db_com = Commentaire(**commentaire.dict(), id_utilisateur=user_id)
    db.add(db_com)
    db.commit()
    db.refresh(db_com)
    return db_com

def get_commentaires_by_ticket(db: Session, ticket_id: int):
    return db.query(Commentaire).filter(Commentaire.id_ticket == ticket_id).all()
