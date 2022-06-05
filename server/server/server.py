import asyncio
import json
import pydantic
from asyncio import transports
from typing import Union

from messages import BaseMessage
from controllers import actions

from models import Base, engine, get_db
from .response import Response


class Server(asyncio.Protocol):
    transport: transports.Transport

    def connection_made(self, transport: transports.Transport):
        self.transport = transport

    def data_received(self, data: bytes) -> None:
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

                response_data = controller["handler"](**args)
                self.write(action, msg.uid, response_data)
                if db is not None:
                    db.close()  # maybe exception
            else:
                response = Response.create_error("Invalid action")
                self.write(action, msg.uid, response)
        except (json.JSONDecodeError, pydantic.ValidationError):
            pass

    def write(self, action: str, uid: str, response: Union[Response, dict]):
        assert isinstance(response, Response) or isinstance(response, dict)

        data: dict = None

        if isinstance(response, Response):
            data = response.get_data()
        elif isinstance(response, dict):
            data = response

        message = {
            "action": action,
            "uid": uid,
            "data": data
        }

        self.transport.write(json.dumps(message).encode("utf-8"))

    @classmethod
    async def run(cls):
        Base.metadata.create_all(bind=engine)
        loop = asyncio.get_running_loop()
        server = await loop.create_server(lambda: cls(), "127.0.0.1", 8080)
        async with server:
            await server.serve_forever()

