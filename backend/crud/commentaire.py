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

def get_commentaire_by_id(db: Session, commentaire_id: int):
    return db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()

def delete_commentaire(db: Session, commentaire_id: int):
    commentaire = db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()
    if commentaire:
        db.delete(commentaire)
        db.commit()


def delete_commentaire(db: Session, commentaire_id: int):
    commentaire = db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()
    if commentaire:
        db.delete(commentaire)
        db.commit()
    return commentaire

def update_commentaire(db: Session, commentaire_id: int, new_contenu: str):
    commentaire = db.query(Commentaire).filter(Commentaire.id == commentaire_id).first()
    if commentaire:
        commentaire.contenu = new_contenu
        db.commit()
        db.refresh(commentaire)
    return commentaire