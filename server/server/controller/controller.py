import inspect


class ControllerMaker:
    actions: dict = {}

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.actions[self.prefix] = {}

    def __call__(self, action: str):
        def decorator(func):
            args = inspect.getfullargspec(func).annotations
            self.actions[self.prefix][action] = {
                "handler": func,
                "args": args,
            }
            return func

        return decorator

    @property
    def controllers(self) -> dict:
        return self.actions[self.prefix]


controller = ControllerMaker("client")
server_controller = ControllerMaker("server")
