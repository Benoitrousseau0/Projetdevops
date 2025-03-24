from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text, nullable=False)
    date_envoi = Column(DateTime, default=datetime.utcnow)
    id_utilisateur = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), nullable=False)
    id_ticket = Column(Integer, ForeignKey("ticket.id", ondelete="SET NULL"), nullable=True)
    lu = Column(Boolean, default=False)

    utilisateur = relationship("Utilisateur")
    ticket = relationship("Ticket", back_populates="notifications")
