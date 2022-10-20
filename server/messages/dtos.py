from typing import List
from server import TokenMessage


class SendMessage(TokenMessage):
    receiver: str
    message: str


class SubscribeMessages(TokenMessage):
    pass


class GetUncheckedMessages(TokenMessage):
    pass


class SetCheckedMessages(TokenMessage):
    messages: List[int]
