from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

class StatutEnum(str, enum.Enum):
    ouvert = "Ouvert"
    en_cours = "En cours"
    resolu = "Résolu"
    ferme = "Fermé"

class PrioriteEnum(str, enum.Enum):
    faible = "Faible"
    moyenne = "Moyenne"
    elevee = "Élevée"
    critique = "Critique"

class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    statut = Column(Enum(StatutEnum), default=StatutEnum.ouvert)
    priorite = Column(Enum(PrioriteEnum), default=PrioriteEnum.moyenne)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_mise_a_jour = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    id_employe = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)

    employe = relationship("Utilisateur")
    commentaires = relationship("Commentaire", back_populates="ticket", cascade="all, delete-orphan")
    techniciens = relationship("TicketTechnicien", back_populates="ticket", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="ticket", cascade="all, delete-orphan")
