from email import message
from functools import wraps
from fastapi import APIRouter, Depends, Request, Response, HTTPException, Security
from .helper import *
from .dependencies import get_decoded_token_data
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

import os

security = HTTPBearer()


def auth_required(post):
    def decorator_factory(func):
        @wraps(func)
        def decorator(request: Request,credentials, *args, **kwargs):
            print("inside decorator //////////////////")
            decode_existing_token = get_decoded_token_data(credentials)
            request.session["decode_existing_token"] = decode_existing_token


            if (
                decode_existing_token
                and decode_existing_token.get("valid_token")
                and decode_existing_token.get("role") == post
                and decode_existing_token.get("is_varified")
            ):
                pass
            else:
                return {"message":"invalid token or not validate for this route please HTTPBearer token for authorizations"}

            return func(request,*args, **kwargs)

        return decorator

    return decorator_factory



def auth_required_nonverified_user(post):
    def decorator_factory(func):
        @wraps(func)
        def decorator(request: Request,credentials, *args, **kwargs):
            print("inside decorator //////////////////")
            decode_existing_token = get_decoded_token_data(credentials)
            request.session["decode_existing_token"] = decode_existing_token
            print("inside decorator //////////////////")
            if (
                decode_existing_token
                and decode_existing_token.get("valid_token")
                and decode_existing_token.get("role") in post
            ):
                pass
            else:
                return {"message":"invalid token or not validate for this route please HTTPBearer token for authorizations"}


            return func(request,*args, **kwargs)

        return decorator

    return decorator_factory