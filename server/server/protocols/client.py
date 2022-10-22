import asyncio

from server.controller import controller
from .handler import handler
from .transport import TcpTransport


class ClientProtocol:
    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        transport = TcpTransport(writer)
        while True:
            data = await reader.read(8192)
            await handler(data, controller.actions, transport)

    async def run(self, host: str, port: int):
        server = await asyncio.start_server(self.handle, host, port)
        async with server:
            await server.serve_forever()
