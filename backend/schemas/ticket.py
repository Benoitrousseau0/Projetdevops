from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import List, Optional
from .utilisateur import UtilisateurOut

class StatutEnum(str, Enum):
    ouvert = "Ouvert"
    en_cours = "En cours"
    resolu = "Résolu"
    ferme = "Fermé"

class PrioriteEnum(str, Enum):
    faible = "Faible"
    moyenne = "Moyenne"
    elevee = "Élevée"
    critique = "Critique"

class TicketBase(BaseModel):
    titre: str
    description: str
    priorite: PrioriteEnum = PrioriteEnum.moyenne

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    titre: Optional[str]
    description: Optional[str]
    statut: Optional[StatutEnum]
    priorite: Optional[PrioriteEnum]

class TicketOut(TicketBase):
    id: int
    statut: StatutEnum
    date_creation: datetime
    date_mise_a_jour: datetime
    id_employe: int
    techniciens: List[int] = []

    class Config:
        orm_mode = True
