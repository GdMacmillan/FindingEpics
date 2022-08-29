from sqlalchemy import Column, Integer, Boolean, Float, String, PickleType, DateTime

from .database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    resource_state = Column(Integer)
    athlete = Column(PickleType)
    distance = Column(Float)
    moving_time = Column(Integer)
    elapsed_time = Column(Integer)
    total_elevation_gain = Column(Float)
    type = Column(String)
    sport_type = Column(String)
    workout_type = Column(Integer)
    start_date = Column(String)
    start_date_local = Column(String)
    timezone = Column(String)
    utc_offset = Column(String)
    location_city = Column(String)
    location_state = Column(String)
    location_country = Column(String)
    achievement_count = Column(Integer)
    kudos_count = Column(Integer)
    comment_count = Column(Integer)
    athlete_count = Column(Integer)
    photo_count = Column(Integer)
    map = Column(PickleType)
    trainer = Column(Boolean)
    commute = Column(Boolean)
    manual = Column(Boolean)
    private = Column(Boolean)
    visibility = Column(String)
    flagged = Column(Boolean)
    gear_id = Column(String)
    start_latlng = Column(PickleType)
    end_latlng = Column(PickleType)
    average_speed = Column(Float)
    max_speed = Column(Float)
    average_temp = Column(Integer)
    average_watts = Column(Float)
    average_cadence = Column(Float)
    average_heartrate = Column(Float)
    max_heartrate = Column(Float)
    max_watts = Column(Float)
    weighted_average_watts = Column(Integer)
    kilojoules = Column(Float)
    device_watts = Column(Boolean)
    has_heartrate = Column(Boolean)
    heartrate_opt_out = Column(Boolean)
    display_hide_heartrate_option = Column(Boolean)
    elev_high = Column(Float)
    elev_low = Column(Float)
    upload_id = Column(Integer)
    upload_id_str = Column(String)
    external_id = Column(String)
    from_accepted_tag = Column(Boolean)
    pr_count = Column(Integer)
    total_photo_count = Column(Integer)
    has_kudoed = Column(Boolean)
    suffer_score = Column(Integer)
    # 


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    resource_state = Column(Integer)
    firstname = Column(String)
    lastname = Column(String)
    bio = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    sex = Column(String)
    premium = Column(Boolean)
    summit = Column(Boolean)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    badge_type_id = Column(Integer)
    weight = Column(Float)
    profile_medium = Column(String)
    profile = Column(String)
    friend = Column(Boolean)
    follower = Column(Boolean)


class Token(Base):
    __tablename__ = "tokens"

    athlete_id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    token_type = Column(String)
    expires_at = Column(Integer)
    expires_in = Column(Integer)