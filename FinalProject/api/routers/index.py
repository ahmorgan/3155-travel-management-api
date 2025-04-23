from . import trips


def load_routes(app):
    app.include_router(trips.router)
