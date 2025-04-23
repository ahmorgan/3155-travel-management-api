from . import user, user_trip_link


def load_routes(app):
    app.include_router(user.router)
    app.include_router(user_trip_link.router)