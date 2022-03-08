from pydantic import BaseModel


class BaseMessage(BaseModel):
    action: str
