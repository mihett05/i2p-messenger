import asyncio


class InterServerProtocol(asyncio.DatagramProtocol):
    transport: asyncio.DatagramTransport

    def datagram_received(self, data: bytes, addr: tuple[str, int]) -> None:
        pass

    @classmethod
    async def run(cls, host: str, port: int, loop: asyncio.AbstractEventLoop):
        server = await loop.create_server(lambda: cls(), host, port)
        async with server:
            await server.serve_forever()
