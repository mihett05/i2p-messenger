import asyncio
import asyncio_dgram
from server.controller import server_controller
from .handler import handler
from .transport import UdpTransport


class InterServerProtocol:
    async def handler(self, stream: asyncio_dgram.DatagramServer):
        while True:
            data, addr = await stream.recv()
            transport = UdpTransport(stream, addr)
            asyncio.create_task(handler(data, server_controller.actions, transport))

    async def run(self, host: str, port: int):
        stream = await asyncio_dgram.bind((host, port))
        asyncio.create_task(self.handler(stream))



