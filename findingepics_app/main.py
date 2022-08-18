import json
import os
import pdb
from pipes import Template
from typing import Optional, List, Union
from fastapi import Depends, FastAPI, Request, Response, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError

from . import crud, models, schemas
from .database import SessionLocal, engine

HERE = os.path.basename(os.path.dirname(__file__))

# Note: before production make migrations using alembic
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

config = Config(os.path.join(os.path.dirname(HERE), '.env.local'))

oauth = OAuth(config)
oauth.register(
    'strava',
    access_token_url='https://www.strava.com/oauth/token',
    access_token_param=None,
    authorize_url='https://www.strava.com/oauth/authorize',
    authorize_params=None,
    api_base_url='https://www.strava.com/api/v3/',
    client_kwargs={'scope': 'activity:read'},
)

app.add_middleware(SessionMiddleware, secret_key="!secret")

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


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.strava.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    kwargs = {
        'client_id': oauth.strava.client_id,
        'client_secret': oauth.strava.client_secret,
        'grant_type': 'authorization_code',
        'f': 'json',
    }

    token = await oauth.strava.authorize_access_token(request, **kwargs)
    print(token)