from typing import Union

from fastapi import FastAPI

import db

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/family/{surname}")
def get_family_by_surname(surname: str):
    names = db.get_family_by_surname(surname)
    return {"status": "ok", "result": names}