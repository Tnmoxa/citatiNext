import os
from contextlib import asynccontextmanager, contextmanager
from starlette.requests import Request
import logging
from starlette.exceptions import HTTPException
from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    AuthCredentials
)
from starlette.responses import JSONResponse
import notifier.client


@asynccontextmanager
async def JsonParams(request: Request):
    """ Helps to use parameters received in JSON body.
    """
    try:
        params = await request.form()
        yield params
    except (AttributeError, KeyError, ValueError) as exc:
        msg = f"Bad request parameters. {exc}"
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.exception(msg)
        else:
            logging.warning(msg)
        raise HTTPException(400, msg)


@contextmanager
def QueryParams(request: Request):
    """ Helps to use query parameters.
    """
    try:
        yield request.query_params._dict
    except (TypeError, AttributeError, KeyError) as exc:
        msg = f"Bad request parameters. {exc}"
        if logging.root.isEnabledFor(logging.DEBUG):
            logging.exception(msg)
        else:
            logging.warning(msg)
        raise HTTPException(400, msg)


async def send_by_email_after_registration(request):
    a = notifier.client.NotificationClient(port=9900, host='localhost')
    try:
        await a.send_by_email_after_registration(request)
    except Exception:
        raise Exception('Server is not available')


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if not request.cookies.get('auth'):
            return
        login = request.cookies.get('auth')
        return AuthCredentials(['authenticated']), SimpleUser(login)

