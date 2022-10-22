import asyncio
import asyncio_dgram
from abc import abstractmethod


class Transport:
    @abstractmethod
    async def send(self, data: bytes):
        pass

    @abstractmethod
    def close(self):
        pass


class TcpTransport(Transport):
    def __init__(self, writer: asyncio.StreamWriter):
        self.writer = writer

    async def send(self, data: bytes):
        self.writer.write(data)
        await self.writer.drain()

    def close(self):
        self.writer.close()

    def is_closing(self) -> bool:
        return self.writer.is_closing()


class UdpTransport(Transport):
    def __init__(self, stream: asyncio_dgram.DatagramServer, addr: (str, int)):
        self.stream = stream
        self.address = addr
        self.host = self.address[0]

    async def send(self, data: bytes):
        await self.stream.send(data, self.address)

    def close(self):
        self.stream.close()
