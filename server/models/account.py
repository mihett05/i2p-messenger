from passlib.context import CryptContext
from typing import Optional
from datetime import datetime
from jose import jwt

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.session import Session

from server.settings import get_settings
from .base import Base


pwd_context = CryptContext(schemes=["bcrypt"])
settings = get_settings()


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    @classmethod
    def create(cls, db: Session, login: str, password: str) -> Optional["Account"]:
        if db.query(cls).filter(login=login).first() is None:
            account = cls(login=login, hashed_password=cls.hash_password(password))
            db.add(account)
            db.commit()
            return account

    @classmethod
    def get_by_id(cls, db: Session, account_id: int) -> Optional["Account"]:
        return db.query(cls).filter(id=account_id).first()

    @classmethod
    def get_by_login(cls, db: Session, login: str) -> Optional["Account"]:
        return db.query(cls).filter(login=login).first()

    @classmethod
    def get_by_token(cls, db: Session, token: str) -> Optional["Account"]:
        data = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if "sub" in data:
            return cls.get_by_login(db, data["sub"])

    @classmethod
    def authenticate(cls, db: Session, login: str, password: str) -> Optional["Account"]:
        account = cls.get_by_login(db, login)
        if account and account.verify_password(password):
            return account

    def create_access_token(self):
        data = {
            "sub": self.login,
            "exp": datetime.utcnow() + settings.JWT_EXPIRE
        }
        return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
