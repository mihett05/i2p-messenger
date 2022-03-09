import asyncio
import json
import pydantic
from asyncio import transports

from messages import BaseMessage
from controllers import actions

from models import Base, engine, get_db


class Server(asyncio.Protocol):
    transport: transports.Transport

    def connection_made(self, transport: transports.Transport):
        self.transport = transport

    def data_received(self, data: bytes) -> None:
        raw_data = data.decode()
        try:
            data = json.loads(raw_data)
            action = BaseMessage(**data).action
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
                response = {
                    "action": action,
                    "data": response_data
                }
                self.transport.write(response)

                if db is not None:
                    db.close()  # maybe exception
            else:
                pass  # Should be error
        except (json.JSONDecodeError, pydantic.ValidationError):
            pass

    @classmethod
    async def run(cls):
        Base.metadata.create_all(bind=engine)
        loop = asyncio.get_running_loop()
        server = await loop.create_server(lambda: cls(), "127.0.0.1", 8080)
        async with server:
            await server.serve_forever()

