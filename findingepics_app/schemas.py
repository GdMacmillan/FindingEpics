from pydantic import BaseModel


class ActivityBase(BaseModel):
    name: str
    elapsed_time: int # seconds
    description: str | None = None
    type: str | None = None


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    athlete: dict

    class Config:
        orm_mode = True


class AthleteBase(BaseModel):
    id: int
    username: str
    resource_state: int


class AthleteCreate(AthleteBase):
    firstname: str | None = None
    lastname: str | None = None
    bio: str | None = None
    city: str | None = None
    state: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    athlete_id: int
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: int
    expires_in: int