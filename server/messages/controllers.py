import asyncio
import json
from typing import Dict
from sqlalchemy.orm import Session

from server import controller
from accounts.models import Account
from .models import Message
from .dtos import (
    SendMessage,
    SubscribeMessages,
    GetUncheckedMessages,
    SetCheckedMessages,
)
from server.response import Response
from nodes.models import Node


class Subscriptions:
    _instance = None
    subscribers: Dict[str, asyncio.Transport]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Subscriptions, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.subscribers = {}

    def write_to_subscriber(self, key: str, data: dict) -> bool:
        if key in self.subscribers:
            if self.subscribers[key].is_closing():
                self.subscribers.pop(key)
            else:
                raw_msg = json.dumps(data).encode("utf-8")
                self.subscribers[key].write(raw_msg)
                return True
        return False

    def subscribe(self, account: Account, transport: asyncio.Transport):
        if account.username in self.subscribers:
            self.write_to_subscriber(
                account.username,
                {
                    "action": "subscription_closed",
                    "uid": "",
                    "data": {"error": "Connection from another client"},
                },
            )
            self.subscribers[account.username].close()
        self.subscribers[account.username] = transport

    def send(
        self, db: Session, sender: str, receiver: Account, message: str, node: Node
    ) -> bool:
        msg = Message.create(db, sender, receiver, message)
        if msg:
            data = {
                "action": "subscribe_messages",
                "uid": "",
                "data": {
                    "from": sender,
                    "server": node.server_hash,
                    "message": message,
                    "date": msg.send_date.timestamp(),
                },
            }
            self.write_to_subscriber(receiver.username, data)
            return True
        return False


@controller("send_message")
def send_message(data: SendMessage, db: Session):
    receiver = Account.get_by_token(db, data.token)
    sender = Account.get_by_login(db, data.receiver)
    return Response(ok=Subscriptions().send(db, sender, receiver, data.message))


@controller("get_unchecked_messages")
def get_unchecked_messages(data: GetUncheckedMessages, db: Session):
    user = Account.get_by_token(db, data.token)
    unchecked = (
        db.query(Message).filter(Message.checked == False, receiver=user.id).all()
    )
    return Response(messages=unchecked)


@controller("set_checked_messages")
def set_checked_messages(data: SetCheckedMessages, db: Session):
    user = Account.get_by_token(db, data.token)
    messages = Message.__table__
    (
        messages.update()
        .where(messages.c.receiver == user.id)
        .where(messages.c.checked == False)
        .values(checked=True)
    )
    return Response()


@controller("subscribe_messages")
def subscribe_messages(
    data: SubscribeMessages, db: Session, transport: asyncio.Transport
):
    user = Account.get_by_token(db, data.token)
    Subscriptions().subscribe(user, transport)
    return Response()
