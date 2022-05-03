from email import message
from functools import wraps
from fastapi import Request
from .helper import *
from .dependencies import get_decoded_token_data

import jwt

import os

templates = Jinja2Templates(directory="app/templates")

templates.env.globals["get_flashed_messages"] = get_flashed_messages


def auth_required(post):
    def decorator_factory(func):
        @wraps(func)
        def decorator(request: Request, *args, **kwargs):
            decode_existing_token = get_decoded_token_data(request)

            if (
                decode_existing_token
                and decode_existing_token.get("valid_token")
                and decode_existing_token.get("role") == post
            ):
                pass
            else:
                return {"message":"please login"}

            return func(request, *args, **kwargs)

        return decorator

    return decorator_factory