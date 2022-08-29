from fastapi import Depends
from fastapi import FastAPI

from .jwt import get_current_user_athlete_id


api_app = FastAPI()

@api_app.get('/')
def test():
    return {'message': 'unprotected api_app endpoint'}


@api_app.get('/protected')
def test2(current_athlete_id: str = Depends(get_current_user_athlete_id)):
    return {'message': 'protected api_app endpoint'}