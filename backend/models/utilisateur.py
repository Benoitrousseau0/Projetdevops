from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from core.database import Base
import enum

class RoleEnum(str, enum.Enum):
    employe = "employe"
    technicien = "technicien"
    admin = "admin"

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    date_inscription = Column(DateTime, default=datetime.utcnow)
