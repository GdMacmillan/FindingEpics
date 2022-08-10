from sqlalchemy.orm import Session

from . import models, schemas


def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()


# def get_athlete_activities(db: Session, athlete_id: int):
#     return db.query(models.Activity).filter(models.Athlete.id == athlete_id).first()


# def get_activities(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Activity).offset(skip).limit(limit).all()


# def get_athlete(db: Session, athlete_id: int):
#     return db.query(models.Athlete).filter(models.Athlete.id == athlete_id).first()


# def get_athlete_by_email(db: Session, email: str):
#     return db.query(models.Athlete).filter(models.Athlete.email == email).first()



# def create_athlete(db: Session, athlete: schemas.AthleteCreate):
#     fake_hashed_password = athlete.password + "notreallyhashed"
#     db_athlete = models.Athlete(email=athlete.email, hashed_password=fake_hashed_password)
#     db.add(db_athlete)
#     db.commit()
#     db.refresh(db_athlete)
#     return db_athlete


# def create_athlete_activity(db: Session, activity: schemas.ActivityCreate, athlete_id: int):
#     db_activity = models.Activity(**activity.dict(), owner_id=athlete_id)
#     db.add(db_activity)
#     db.commit()
#     db.refresh(db_activity)
#     return db_activity
