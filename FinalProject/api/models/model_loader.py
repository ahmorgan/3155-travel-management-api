from . import trips, user, user_trip_link, booking
from ..dependencies.database import engine


def index():
    trips.Base.metadata.create_all(engine)
    user.Base.metadata.create_all(engine)
    user_trip_link.Base.metadata.create_all(engine)
    booking.Base.metadata.create_all(engine)

