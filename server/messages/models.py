from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import Session
from datetime import datetime

from server import Base
from nodes.models import Node


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, nullable=False)
    sender_host = Column(String, ForeignKey("nodes.host"), nullable=False)
    receiver = Column(String, ForeignKey("accounts.username"), nullable=False)
    message = Column(String)
    checked = Column(Boolean, default=False)

    send_date = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def create(
        cls,
        db: Session,
        sender: str,
        receiver: str,
        message: str,
        sender_host: str = None,
    ) -> "Message":
        node = (
            db.query(Node)
            .filter(Node.host == sender_host or Node.get_current_host())
            .first()
        )  # current host exists always
        if not node:
            node = Node.create(db, sender_host)

        msg = Message(
            sender=sender,
            receiver=receiver,
            message=message,
            sender_host=node.host,
        )
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
