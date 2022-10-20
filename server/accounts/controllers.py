from sqlalchemy.orm import Session
from server import controller
from .dtos import CreateAccount, SigninAccount
from .models import Account
from server.response import Response


def create_account_response(account: Account) -> Response:
    if account:
        return Response(
            token=account.create_access_token(),
            id=account.id,
            login=account.username
        )
    return Response.create_error("Can't create account")


@controller("create_account")
def create_account(data: CreateAccount, db: Session):
    account = Account.create(db, data.login, data.password)
    return create_account_response(account)


@controller("signin_account")
def sign_in_account(data: SigninAccount, db: Session):
    account = Account.authenticate(db, data.login, data.password)
    return create_account_response(account)
