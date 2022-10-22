from datetime import datetime
from typing import Optional, List
from hashlib import md5

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session
from pydantic import BaseModel

from server import Base


class Node(Base):
    _current_host: "Node" = None

    __tablename__ = "nodes"

    host = Column(String, primary_key=True, unique=True)
    found_date = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.now)
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

    @classmethod
    def get_all(cls, db: Session) -> List["Node"]:
        return db.query(cls).all()

    @classmethod
    def get_by_host(cls, db: Session, host: str) -> "Node":
        if node := db.query(Node).where(Node.host == host).first():
            return node
        return Node.create(db, host)

    def update_time(self, db: Session):
        self.last_active = datetime.now()
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()


class NodeDto(BaseModel):
    host: str
    found_date: datetime
    last_active: datetime
    server_hash: str

    class Config:
        orm_mode = True
