import json
import os
import pathlib
from pipes import Template
from typing import Optional, List, Union
from fastapi import Depends, FastAPI, Request, Response, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

HERE = os.path.basename(os.path.dirname(__file__))

# Note: before production make migrations using alembic
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(HERE, "templates"))


@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_activities = db.query(models.Activity).count()
    if num_activities == 0:
        with open("activities.json") as f:
            data = json.load(f)

        for activity in data:
            db.add(models.Activity(**activity))
        db.commit()
    else:
        print(f"number of activities in db: {num_activities}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/index/", response_class=HTMLResponse)
def get_index(
    request: Request,
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db),
    page: int = 1,
):
    n = 2
    offset = (page - 1) * n
    activities = db.query(models.Activity).offset(offset).limit(n)
    context = {"request": request, "activities": activities, "page": page}
    if hx_request:
        return templates.TemplateResponse("table.html", context)

    return templates.TemplateResponse("index.html", context)


@app.get("/activities/{activity_id}", response_class=HTMLResponse)
def activity(
    request: Request,
    activity_id: int,
    db: Session = Depends(get_db)
):
    db_activity = crud.get_activity(db, activity_id=activity_id)
    context = {"request": request, "activity": db_activity._asdict()}
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    return templates.TemplateResponse("activity.html", context)