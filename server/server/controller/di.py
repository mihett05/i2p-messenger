from sqlalchemy.orm import Session

from server.protocols.transport import Transport
from messages.channels import Channels
from accounts.models import Account


class DI:
    @staticmethod
    def transport(cls: type, data: dict, transport: Transport, db: Session):
        return transport

    @staticmethod
    def db(cls: type, data: dict, transport: Transport, db: Session):
        return db

    @staticmethod
    def data(cls: type, data: dict, transport: Transport, db: Session):
        return cls(**data)

    @staticmethod
    def channels(cls: type, data: dict, transport: Transport, db: Session):
        return Channels()

    @staticmethod
    def account(cls: type, data: dict, transport: Transport, db: Session):
        return Account.get_by_token(db, data["token"])


def provide_di(controller: dict, data: dict, transport: Transport, db: Session) -> dict:
    return {
        arg: getattr(DI, arg)(cls, data, transport, db)
        for arg, cls in controller["args"].items()
        if hasattr(DI, arg)
    }
