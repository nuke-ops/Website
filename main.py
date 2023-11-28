import json
import logging
import re
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError
from sqlalchemy import desc
from sqlalchemy.orm import Session

import models
from database import diceEngine, get_db

app = FastAPI(debug=True)

origins = [
    "https://nukeops.com.com",
    "http://127.0.0.1:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socket_base_url = "ws://127.0.0.1:8000/ws" if app.debug else "wss://nukeops.com/ws"


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

models.Base.metadata.create_all(bind=diceEngine)


connected_clients: list[WebSocket] = []

##
## Main
##


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("main/main.html", {"request": request})


@app.get("/ss13")
async def main_ss13(request: Request):
    return templates.TemplateResponse("main/ss13.html", {"request": request})


@app.get("/ss13/rules")
async def main_ss13_rules(request: Request):
    return templates.TemplateResponse("main/rules.html", {"request": request})


##
## Others
##


@app.get("/robots.txt")
async def robotsTxt(request: Request):
    return FileResponse("static/robots.txt")


@app.get("/sitemap.xml")
async def sitemapXml(request: Request):
    return FileResponse("static/sitemap.xml")


#
# errors
#


@app.exception_handler(Exception)
async def handle_error(request: Request, exc: Exception):
    error_code = getattr(exc, "code", 500)
    error_detail = None

    if error_code == 400:
        error_detail = f"{error_code} - BAD REQUEST"
    elif error_code == 401:
        error_detail = f"{error_code} - AUTH REQUIRED"
    elif error_code == 403:
        error_detail = f"{error_code} - PAGE FORBIDDEN"
    elif error_code == 404:
        error_detail = f"{error_code} - PAGE NOT FOUND"

    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error_code": error_detail},
        status_code=error_code,
    )


##
## Dice
##


@app.get("/dice", response_class=HTMLResponse)
async def dice(request: Request, db: Session = Depends(get_db)):
    dice_records = db.query(models.Dice).order_by(desc(models.Dice.id)).limit(10).all()
    return templates.TemplateResponse(
        "dice/dice.html",
        {
            "request": request,
            "dice_records": dice_records,
            "socket_base_url": socket_base_url,
        },
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    finally:
        connected_clients.remove(websocket)


class DiceCreate(BaseModel):
    name: str
    dice: int
    sides: int
    throws: str
    sum: int
    modifier: Optional[str]


def dice_data_validation(data) -> None:
    try:
        for key, value in json.loads(data).items():
            # check if ints are ints
            if key in ["dice", "sides", "sum"] and type(value) != int:
                raise InvalidDiceFormatError()

            if type(value) == str:
                # check the pattern "{mod}({+/-}{number})"
                if key == "modifier":
                    if (
                        not re.match(r"^(str|int|dex|con|wis|cha)\([+-]\d+\)$", value)
                        and value != ""
                    ):
                        raise InvalidDiceFormatError()

                # pass only numbers and ,
                if key == "throws":
                    if not re.match(r"^[0-9, ]+$", value):
                        raise InvalidDiceFormatError()

                # pass only alphanumeric
                if not re.match(r"^[0-9a-zA-Z,+\- ]+$", value) and key not in [
                    "modifier",
                    "throws",
                ]:
                    raise InvalidDiceFormatError()
    except Exception as e:
        print(f"Error: {e}")
        raise InvalidDiceFormatError()


class InvalidDiceFormatError(Exception):
    def __init__(self, message="Invalid dice format"):
        self.message = message
        super().__init__(self.message)


@app.post("/api/insert_dice_roll")
async def insert_dice_roll(data: DiceCreate, db: Session = Depends(get_db)):
    try:
        dice_data_validation(data.model_dump_json())
        db_dice = models.Dice(**data.model_dump())
        db.add(db_dice)
        db.commit()
        db.refresh(db_dice)

        for client in connected_clients:
            await client.send_text("update")

        return db_dice
    except InvalidDiceFormatError as e:
        raise HTTPException(status_code=422, detail="Invalid dice format")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/api/get_dice_rolls")
async def get_dice_rolls(db: Session = Depends(get_db)):
    try:
        dice_records = (
            db.query(models.Dice).order_by(desc(models.Dice.id)).limit(10).all()
        )

        dice_data = [
            {
                "name": record.name,
                "dice": record.dice,
                "sides": record.sides,
                "throws": record.throws,
                "sum": record.sum,
                "modifier": record.modifier,
                "date": record.date.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for record in dice_records
        ]

        return JSONResponse(content=dice_data)
    except Exception as e:
        logging.exception("Error in get_dice_rolls")
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)
