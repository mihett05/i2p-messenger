import inspect


actions = {}


def controller(action: str):
    def decorator(func):
        args = inspect.getfullargspec(func).annotations
        if "data" in args:
            actions[action] = {
                "msg": args["data"],
                "handler": func,
                "need_transport": "transport" in args
            }
        return func
    return decorator

