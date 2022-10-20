import asyncio
import json
import pydantic
from asyncio import transports
from typing import Union

from .message import BaseMessage
from .controller import actions
from .modules import attach_modules

from .database import Base, engine, get_db
from .response import Response

from nodes.models import Node
from nodes.transport import InterServerProtocol


class Server(asyncio.Protocol):
    transport: transports.Transport

    def connection_made(self, transport: transports.Transport):
        self.transport = transport

    async def async_data_received(self, data: bytes):
        raw_data = data.decode()
        try:
            data = json.loads(raw_data)
            msg = BaseMessage(**data)
            action = msg.action
            if action in actions:
                controller = actions[action]
                db = None

                args = {
                    "data": controller["msg"](**data),
                }
                if controller["need_transport"]:
                    args["transport"] = self.transport
                if controller["need_db"]:
                    db = get_db()
                    args["db"] = db

                if asyncio.iscoroutinefunction(controller["handler"]):
                    response_data = await controller["handler"](**args)
                else:
                    response_data = controller["handler"](**args)
                self.write(action, msg.uid, response_data)
                if db is not None:
                    db.close()  # maybe exception
            else:
                response = Response.create_error("Invalid action")
                self.write(action, msg.uid, response)
        except (json.JSONDecodeError, pydantic.ValidationError):
            pass

    def data_received(self, data: bytes):
        asyncio.create_task(self.async_data_received(data))

    def write(self, action: str, uid: str, response: Union[Response, dict]):
        if isinstance(response, Response):
            data = response.get_data()
        elif isinstance(response, dict):
            data = response
        else:
            raise TypeError("response parameter should be either Response or dict")

        message = {"action": action, "uid": uid, "data": data}

        self.transport.write(json.dumps(message).encode("utf-8"))

    @staticmethod
    def init_current_host(host: str):
        # TODO: change host
        db = get_db()
        node = db.query(Node).filter(Node.host == host).first()
        if not node:
            node = Node.create(db, host)
        Node._current_host = node

        if db:
            db.close()

    @classmethod
    async def _run_server(cls, host: str, port: int, loop: asyncio.AbstractEventLoop):
        server = await loop.create_server(lambda: cls(), host, port)
        async with server:
            await server.serve_forever()

    @classmethod
    async def run(
        cls, host: str = "127.0.0.1", port: int = 8080, inter_port: int = 8081
    ):
        attach_modules()
        Base.metadata.create_all(bind=engine)
        loop = asyncio.get_running_loop()
        cls.init_current_host(host)
        loop.create_task(cls._run_server(host, port, loop))
        loop.create_task(InterServerProtocol.run(host, inter_port, loop))
        loop.run_forever()
