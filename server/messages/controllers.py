from sqlalchemy.orm import Session
from sqlalchemy.sql import update

from server import controller
from accounts.models import Account
from .models import Message, MessageDto
from .dtos import (
    SendMessage,
    SubscribeMessages,
    GetUncheckedMessages,
    SetCheckedMessages,
)
from server.response import Response
from server.protocols.transport import TcpTransport
from .channels import Channels


@controller("send_message")
def send_message(data: SendMessage, db: Session, account: Account, channels: Channels):
    receiver = Account.get_by_login(db, data.receiver)
    return Response(ok=channels.send(db, account, receiver, data.message))


@controller("get_unchecked_messages")
def get_unchecked_messages(data: GetUncheckedMessages, db: Session, account: Account):
    unchecked = (
        db.query(Message)
        .where(Message.checked == False)
        .where(Message.receiver == account.id)
        .all()
    )
    return Response(
        messages=[MessageDto.from_orm(message).dict() for message in unchecked]
    )


@controller("set_checked_messages")
def set_checked_messages(data: SetCheckedMessages, db: Session, account: Account):
    db.execute(
        update(Message)
        .where(Message.receiver == account.id)
        .where(Message.checked == False)
        .values(checked=True)
    )
    db.commit()
    return Response()


@controller("connect")
def subscribe_messages(
    data: SubscribeMessages,
    db: Session,
    transport: TcpTransport,
    account: Account,
    channels: Channels,
):
    channels.connect(account, transport)
    return Response()
