from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- Out ---
class NotificationOut(BaseModel):
    id: int
    message: str
    date_envoi: datetime
    id_utilisateur: int
    id_ticket: Optional[int] = None
    lu: bool

    class Config:
        orm_mode = True
