from pydantic import BaseModel
from datetime import datetime

class CommentaireBase(BaseModel):
    contenu: str

class CommentaireCreate(CommentaireBase):
    id_ticket: int

class CommentaireOut(CommentaireBase):
    id: int
    date_commentaire: datetime
    id_ticket: int
    id_utilisateur: int

    class Config:
        orm_mode = True

class CommentaireUpdate(BaseModel):
    contenu: str