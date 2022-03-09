from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from . import Base, Account


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    receiver = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    message = Column(String)
    checked = Column(Boolean, default=False)

    send_date = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, db: Session, sender: Account, receiver: Account, message: str) -> Optional["Message"]:
        if sender and receiver:
            msg = Message(sender=sender.id, receiver=receiver.id, message=message)
            db.add(msg)
            db.commit()
            return msg

    def set_checked(self, db: Session):
        self.checked = True
        db.add(self)
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
