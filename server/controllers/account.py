from .base import controller
from messages.account import CreateAccount, SigninAccount
from models import get_db, Account


def create_account_response(account: Account) -> dict:
    if account:
        return {
            "ok": True,
            "token": account.create_access_token(),
            "id": account.id,
            "login": account.login
        }
    return {
        "ok": False,
        "error": "Can't create account"
    }


@controller("create_account")
def create_account(data: CreateAccount):
    db = get_db()
    account = Account.create(db, data.login, data.password)
    return create_account_response(account)


@controller("signin_account")
def sign_in_account(data: SigninAccount):
    db = get_db()
    account = Account.authenticate(db, data.login, data.password)
    return create_account_response(account)
