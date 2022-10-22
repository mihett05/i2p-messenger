from pydantic import BaseModel


class BaseMessage(BaseModel):
    id: str
    action: str


class GetNodesRequest(BaseMessage):
    action = "get_nodes"


class SendMessageRequest(BaseMessage):
    action = "send_message"
    sender: str
    receiver: str
    message: str
