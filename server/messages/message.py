from typing import List
from .base import TokenMessage


class SendMessage(TokenMessage):
    receiver: str
    message: str


class SubscribeMessages(TokenMessage):
    pass


class GetUncheckedMessages(TokenMessage):
    pass


class SetCheckedMessages(TokenMessage):
    messages: List[int]
