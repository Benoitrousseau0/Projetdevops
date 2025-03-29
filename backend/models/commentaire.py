from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Commentaire(Base):
    __tablename__ = "commentaire"

    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(Text, nullable=False)
    date_commentaire = Column(DateTime, default=datetime.utcnow)
    id_ticket = Column(Integer, ForeignKey("ticket.id", ondelete="CASCADE"), nullable=False)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)

    ticket = relationship("Ticket", back_populates="commentaires")
    utilisateur = relationship("Utilisateur", back_populates="commentaires")
    utilisateur = relationship("Utilisateur")
