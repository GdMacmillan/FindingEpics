import os
import uvicorn
from typing import Optional
from fastapi import Depends, FastAPI, Request, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from findingepics_app import crud, models, schemas
from findingepics_app.api import api_app
from findingepics_app.auth import auth_app
from findingepics_app.database import SessionLocal, engine

HERE = os.path.basename(os.path.dirname(__file__))

# Note: before production make migrations using alembic
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount('/auth', auth_app)
app.mount('/api', api_app)
app.mount("/static", StaticFiles(directory="findingepics_app/static"), name="static")

templates = Jinja2Templates(directory="findingepics_app/templates")


# @app.on_event("startup")
# def startup_populate_db():
#     db = SessionLocal()
#     num_activities = db.query(models.Activity).count()
#     if num_activities == 0:
#         with open("activities.json") as f:
#             data = json.load(f)

#         for activity in data:
#             db.add(models.Activity(**activity))
#         db.commit()
#     else:
#         print(f"number of activities in db: {num_activities}")


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


@app.get("/index/activities/{activity_id}", response_class=HTMLResponse)
def activity(
    request: Request,
    activity_id: int,
    db: Session = Depends(get_db),
):
    db_activity = crud.get_activity(db, activity_id=activity_id)
    context = {"request": request, "activity": db_activity._asdict()}
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    return templates.TemplateResponse("activity.html", context)


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user



# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.get("/users/me")
# async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
#     return current_user





# @app.get("/index/athlete/{athlete_id}")
# def logged_in_athlete(
#     request: Request,
#     activity_id: int,
#     db: Session = Depends(get_db),
# ):
#     pass

@app.get('/')
async def root():
    return HTMLResponse('<body><a href="/auth/login">Log In</a></body>')

@app.get('/token')
async def token(request: Request):
    return HTMLResponse('''
                <script>
                function send(){
                    var req = new XMLHttpRequest();
                    req.onreadystatechange = function() {
                        if (req.readyState === 4) {
                            console.log(req.response);
                            if (req.response["result"] === true) {
                                window.localStorage.setItem('jwt', req.response["athlete_id"]);
                            }
                        }
                    }
                    req.withCredentials = true;
                    req.responseType = 'json';
                    req.open("get", "/auth/token?"+window.location.search.substr(1), true);
                    req.send("");
                }
                </script>
                <button onClick="send()">Get FastAPI JWT Token</button>
                <button onClick='fetch("http://127.0.0.1:8000/api/").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Unprotected API
                </button>
                <button onClick='fetch("http://127.0.0.1:8000/api/protected").then(
                    (r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API without JWT
                </button>
                <button onClick='fetch("http://127.0.0.1:8000/api/protected",{
                    headers:{
                        "Authorization": "Bearer " + window.localStorage.getItem("jwt")
                    },
                }).then((r)=>r.json()).then((msg)=>{console.log(msg)});'>
                Call Protected API wit JWT
                </button>
            ''')

if __name__ == '__main__':
    uvicorn.run(app, port=8000)