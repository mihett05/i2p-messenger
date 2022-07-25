from typing import Any


class Response:
    def __init__(self, ok: bool = True, **kwargs):
        self.data = {
            "ok": ok,
            **kwargs
        }

    def __setitem__(self, key: str, value: Any):
        self.write(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def get(self, key: str) -> Any:
        return self.data[key]

    def write(self, key: str, value: Any):
        self.data[key] = value

    def get_data(self):
        return self.data

    @classmethod
    def create_error(cls, error_message: str) -> "Response":
        response = Response(ok=False)
        response["error"] = error_message
        return response
