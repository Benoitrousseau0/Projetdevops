from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# --- Base ---
class CommentaireBase(BaseModel):
    contenu: str

# --- Create ---
class CommentaireCreate(CommentaireBase):
    id_ticket: int

# --- Update ---
class CommentaireUpdate(BaseModel):
    contenu: Optional[str] = None

# --- Out ---
class CommentaireOut(CommentaireBase):
    id: int
    date_commentaire: datetime
    id_ticket: int
    id_utilisateur: int

    class Config:
        orm_mode = True