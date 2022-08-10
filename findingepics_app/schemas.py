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
