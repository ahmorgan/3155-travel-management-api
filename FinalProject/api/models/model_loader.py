from . import trips
from ..dependencies.database import engine


def index():
    trips.Base.metadata.create_all(engine)
