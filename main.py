import logging
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
    return FileResponse("static/pages/main.html")


@app.get("/robots.txt")
async def robotsTxt(request: Request):
    return FileResponse("static/robots.txt")


@app.get("/sitemap.xml")
async def sitemapXml(request: Request):
    return FileResponse("static/sitemap.xml")


#
# errors
#


@app.exception_handler(400)
async def custom_404_handler(_, __):
    return FileResponse("static/pages/error/400.html")


@app.exception_handler(401)
async def custom_404_handler(_, __):
    return FileResponse("static/pages/error/401.html")


@app.exception_handler(403)
async def custom_404_handler(_, __):
    return FileResponse("static/pages/error/403.html")


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse("static/pages/error/404.html")


@app.exception_handler(500)
async def custom_404_handler(_, __):
    return FileResponse("static/pages/error/500.html")


@app.exception_handler(503)
async def custom_404_handler(_, __):
    return FileResponse("static/pages/error/503.html")


##
## Dice
##


@app.get("/dice", response_class=HTMLResponse)
async def dice(request: Request, db: Session = Depends(get_db)):
    dice_records = db.query(models.Dice).order_by(desc(models.Dice.id)).limit(10).all()
    return templates.TemplateResponse(
        "dice.html",
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
    throws: List[int]
    sum: int
    modifier: Optional[str]


@app.post("/api/insert_dice_roll")
async def insert_dice_roll(data: DiceCreate, db: Session = Depends(get_db)):
    try:
        db_dice = models.Dice(**data.dict())
        db.add(db_dice)
        db.commit()
        db.refresh(db_dice)

        for client in connected_clients:
            await client.send_text("update")

        return db_dice
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=422, detail=e.errors())
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
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
