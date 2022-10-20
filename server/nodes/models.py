from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from hashlib import md5

from server import Base


class Node(Base):
    _current_host: "Node" = None

    __tablename__ = "nodes"

    host = Column(String, primary_key=True, unique=True)
    found_date = Column(DateTime, default=datetime.utcnow)
    last_interacted_date = Column(DateTime, default=datetime.now)
    server_hash = Column(String)

    @staticmethod
    def get_hash(host: str) -> str:
        return md5(host.encode("utf-8")).hexdigest()

    @classmethod
    def get_current_host(cls) -> str:
        return cls._current_host.host

    @classmethod
    def create(cls, db: Session, host: str) -> Optional["Node"]:
        node = Node(host=host, server_hash=cls.get_hash(host))
        db.add(node)
        db.commit()
        return node

    def update_time(self, db: Session):
        self.last_interacted_date = datetime.now()
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
