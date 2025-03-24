from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationOut(BaseModel):
    id: int
    message: str
    date_envoi: datetime
    id_utilisateur: int
    id_ticket: Optional[int]
    lu: bool

    class Config:
        orm_mode = True
