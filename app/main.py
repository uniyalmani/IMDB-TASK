from fastapi import FastAPI, APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes import common, protected
from typing import Optional



tags_metadata = [
    {
        "name": "Common Routes",
        "description": "Common Routes Can be used without any token **HTTPBearer  (http, Bearer)**",
    },
    {
        "name": "Protected Routes",
        "description": "Protected Routes    needs authorizations by setting **HTTPBearer  (http, Bearer)**",
    },
]


middleware = [Middleware(SessionMiddleware, secret_key="ashu")]



app = FastAPI(middleware=middleware, openapi_tags=tags_metadata, docs_url="/documentation")

app.include_router(common.router)

app.include_router(protected.router)





@app.get("/", tags=["main page"])
def home_page(request: Request):
    return RedirectResponse("/documentation", status_code=303)

