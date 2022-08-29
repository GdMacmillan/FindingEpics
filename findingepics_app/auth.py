import os

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import Depends, FastAPI, Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from . import jwt
from .database import SessionLocal

HERE = os.path.basename(os.path.dirname(__file__))


# Create the auth app
auth_app = FastAPI()

# Set up OAuth
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

# Set up the middleware to read the request session
auth_app.add_middleware(SessionMiddleware, secret_key="!secret")

# Frontend URL:
FRONTEND_URL = os.environ.get('FRONTEND_URL') or 'http://127.0.0.1:8000/token'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_app.get("/login")
async def login(request: Request):

    # redirect_uri = request.url_for('auth')
    redirect_uri = FRONTEND_URL
    return await oauth.strava.authorize_redirect(request, redirect_uri)

    # user_data = request.session.get('user')
    # if not user_data:
    #     redirect_uri = request.url_for('auth')
    #     return await oauth.strava.authorize_redirect(request, redirect_uri)
    
    # elif datetime.fromtimestamp(user_data['expires_at']) < datetime.now():
    #     redirect_uri = request.url_for('refresh')
    #     return await oauth.strava.authorize_redirect(request, redirect_uri, refresh_token=user_data['refresh_token'])
    
    # else:
    #     redirect_url = request.url_for('logged_in_athlete', **{'athlete_id': user_data['id']})
    #     return RedirectResponse(redirect_url, status_code=303)


@auth_app.get("/token")
async def auth(request: Request, db: Session = Depends(get_db)):
    kwargs = {
        'client_id': oauth.strava.client_id,
        'client_secret': oauth.strava.client_secret,
        'grant_type': 'authorization_code',
        'f': 'json',
    }
    try:
        user_data = await oauth.strava.authorize_access_token(request, **kwargs)

    except OAuthError:
        raise jwt.CREDENTIALS_EXCEPTION
    
    if jwt.valid_athlete_id_from_db(db, user_data['athlete']['id']):
        return JSONResponse({'result': True, 'athlete_id': jwt.create_token(user_data['athlete']['id'])})
    
    raise jwt.CREDENTIALS_EXCEPTION



# @app.get("/refresh")
# async def refresh(request: Request, db: Session = Depends(main.get_db), refresh_token: str | None = None):
#     user_data = request.session.get('user')
#     kwargs = {
#         'client_id': oauth.strava.client_id,
#         'client_secret': oauth.strava.client_secret,
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token,
#         'f': 'json',
#     }
#     try:
#         updated_token = await oauth.strava.authorize_access_token(request, **kwargs)
#         request.session['user'].update(updated_token)
#         return JSONResponse({'athlete_id': jwt.create_token(user_data['athlete']['id']))})


#     except OAuthError:
#         raise jwt.CREDENTIALS_EXCEPTION