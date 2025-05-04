from . import trips, user, user_trip_link, review, booking
from . import trips, user, user_trip_link, review


def load_routes(app):
    app.include_router(trips.router)
    app.include_router(user.router)
    app.include_router(user_trip_link.router)
    app.include_router(booking.router)
    app.include_router(review.router)
