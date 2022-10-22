import json
import asyncio
import pydantic
from typing import Union

from server.message import BaseMessage
from server.response import Response
from server.database import get_db
from .transport import Transport
from server.controller.di import provide_di


async def write(
    transport: asyncio.Transport, action: str, uid: str, response: Union[Response, dict]
):
    if isinstance(response, Response):
        data = response.get_data()
    elif isinstance(response, dict):
        data = response
    else:
        raise TypeError("response parameter should be either Response or dict")

    message = {
        "action": action,
        "uid": uid,
        "data": data,
    }

    transport.write(json.dumps(message).encode("utf-8"))


async def handler(encoded_data: bytes, actions: dict, transport: Transport):
    raw_data = encoded_data.decode()
    try:
        data = json.loads(raw_data)
        msg = BaseMessage(**data)
        action = msg.action
        if action in actions:
            controller = actions[action]
            with get_db() as db:
                args = provide_di(controller, data, transport, db)

                if asyncio.iscoroutinefunction(controller["handler"]):
                    response_data = await controller["handler"](**args)
                else:
                    response_data = controller["handler"](**args)

                await write(transport, action, msg.uid, response_data)
        else:
            response = Response.create_error("Invalid action")
            await write(transport, action, msg.uid, response)
    except (json.JSONDecodeError, pydantic.ValidationError):
        pass
