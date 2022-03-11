from pydantic import BaseModel


class BaseMessage(BaseModel):
    action: str
    uid: str


class TokenMessage(BaseMessage):
    token: str
