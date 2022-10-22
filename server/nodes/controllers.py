from sqlalchemy.orm import Session

from server.controller import server_controller
from server.response import Response
from .dtos import GetNodesRequest, SendMessageRequest
from .models import Node, NodeDto
from accounts.models import Account
from messages.channels import Channels
from server.protocols.transport import UdpTransport


@server_controller("get_nodes")
def get_nodes(data: GetNodesRequest, db: Session):
    return Response(nodes=[NodeDto.from_orm(node).dict() for node in Node.get_all(db)])


@server_controller("send_message")
def send_message(
    data: SendMessageRequest, db: Session, transport: UdpTransport, channels: Channels
):
    receiver = Account.get_by_login(db, data.receiver)
    node = Node.get_by_host(db, transport.host)
    if channels.send(
        db,
        data.sender,
        receiver,
        data.message,
        node
    ):
        return Response()
    return Response(False, message="Failed to create message")
