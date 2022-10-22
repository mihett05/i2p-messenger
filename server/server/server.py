import asyncio

from .modules import attach_modules

from .database import Base, engine, get_db

from nodes.models import Node
from .protocols import ClientProtocol, InterServerProtocol


class Server:
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
    async def run(
        cls, host: str = "127.0.0.1", port: int = 8080, inter_port: int = 8081
    ):
        attach_modules()
        Base.metadata.create_all(bind=engine)
        loop = asyncio.get_running_loop()
        cls.init_current_host(host)
        loop.create_task(ClientProtocol().run(host, port))
        loop.create_task(InterServerProtocol().run(host, inter_port))
        loop.run_forever()
