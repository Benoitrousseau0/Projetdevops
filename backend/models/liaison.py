from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship
from core.database import Base

class TicketTechnicien(Base):
    __tablename__ = "ticket_technicien"

    id_ticket = Column(Integer, ForeignKey("ticket.id", ondelete="CASCADE"), primary_key=True)
    id_technicien = Column(Integer, ForeignKey("utilisateur.id", ondelete="CASCADE"), primary_key=True)

    ticket = relationship("Ticket", back_populates="techniciens")
    technicien = relationship("Utilisateur")
