from server import BaseMessage


class BaseAccount(BaseMessage):
    login: str
    password: str


class CreateAccount(BaseAccount):
    action = "create_account"


class SigninAccount(BaseAccount):
    action = "signin_account"

