from . import trips, user, user_trip_link
from ..dependencies.database import engine


def index():
    trips.Base.metadata.create_all(engine)
    user.Base.metadata.create_all(engine)
    user_trip_link.Base.metadata.create_all(engine)
