import json
from typing import Dict
from sqlalchemy.orm import Session
from uuid import uuid4

from accounts.models import Account
from .models import Message
from server.protocols.transport import TcpTransport
from nodes.models import Node


class Channels:
    _instance = None
    listeners: Dict[str, TcpTransport]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Channels, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.listeners = {}

    def write(self, key: str, data: dict) -> bool:
        if key in self.listeners:
            if self.listeners[key].is_closing():
                self.listeners.pop(key)
            else:
                raw_msg = json.dumps(data).encode("utf-8")
                self.listeners[key].send(raw_msg)
                return True
        return False

    def connect(self, account: Account, transport: TcpTransport):
        if account.username in self.listeners:
            self.write(
                account.username,
                {
                    "action": "channel_closed",
                    "uid": str(uuid4()),
                    "data": {
                        "error": "Connection from another client",
                    },
                },
            )
            self.listeners[account.username].close()
        self.listeners[account.username] = transport

    def send(
        self,
        db: Session,
        sender: str,
        receiver: Account,
        message: str,
        node: Node = None,
    ) -> bool:
        if not node:
            node = Node.get_current_host()
        msg = Message.create(db, sender, receiver, message)
        if msg:
            data = {
                "action": "message",
                "uid": str(uuid4()),
                "data": {
                    "from": sender,
                    "server": node.server_hash,
                    "message": message,
                    "date": msg.send_date.timestamp(),
                },
            }
            self.write(receiver.username, data)
            return True
        return False
