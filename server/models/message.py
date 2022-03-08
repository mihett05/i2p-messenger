from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from .base import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    receiver = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    message = Column(String)
    checked = Column(Boolean)
