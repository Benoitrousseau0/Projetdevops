from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import List, Optional

# --- Enums ---
class StatutEnum(str, Enum):
    ouvert = "ouvert"
    en_cours = "en_cours"
    resolu = "resolu"
    ferme = "ferme"

class PrioriteEnum(str, Enum):
    faible = "faible"
    moyenne = "moyenne"
    elevee = "elevee"
    critique = "critique"

# --- Base ---
class TicketBase(BaseModel):
    titre: str
    description: str
    priorite: PrioriteEnum = PrioriteEnum.moyenne

# --- Create ---
class TicketCreate(TicketBase):
    pass

# --- Update ---
class TicketUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    statut: Optional[StatutEnum] = None
    priorite: Optional[PrioriteEnum] = None

# --- Out ---
class TicketOut(TicketBase):
    id: int
    statut: StatutEnum
    date_creation: datetime
    date_mise_a_jour: Optional[datetime] = None
    id_employe: int
    techniciens: List[int] = []

    class Config:
        orm_mode = True
