from fastapi import FastAPI

from pydantic import BaseModel

from typing import Optional

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.put("/", tags=["main page"])
def home_page(item:Item):
    return {"message": "running", "item":item}