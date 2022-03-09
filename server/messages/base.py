from pydantic import BaseModel


class BaseMessage(BaseModel):
    action: str


class TokenMessage(BaseMessage):
    token: str
