from fastapi.testclient import TestClient
from ..controllers import trips, user, user_trip_link
from ..main import app
import pytest
from .. import main
import json

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_recommend_trip(db_session):
    new_user = {
        "user_id": 100,
        "username": "mr. john",
        "password": "bigguy2000"
    }
    user.create(db_session, new_user)

    # deterministic system should yield (Brazil, Nature) for trips 1,2,
    # as it did for user_id 4
    new_trip_links = [
        {
            "user_id": 100,
            "trip_id": 1,
            "date_booked": "2025-05-01T18:04:19.193Z"
        },
        {
            "user_id": 100,
            "trip_id": 2,
            "date_booked": "2025-05-01T18:04:19.193Z"
        }
    ]
    for link in new_trip_links:
        user_trip_link.create(db_session, link)

    rec = main.recommend_trip(user_id=100)

    assert rec["country"] == "Brazil"
    assert rec["category"] == "Nature"

    new_user = {
        "username": "mr. john 2",
        "password": "bigguy3000",
        "user_id": 101
    }
    user.create(db_session, new_user)
    new_trip_links = [
        {
            "user_id": 101,
            "trip_id": 123,
            "date_booked": "2025-05-01T18:04:19.193Z"
        },
        {
            "user_id": 101,
            "trip_id": 362,
            "date_booked": "2025-05-01T18:04:19.193Z"
        },
        {
            "user_id": 101,
            "trip_id": 313,
            "date_booked": "2025-05-01T18:04:19.193Z"
        },
        {
            "user_id": 101,
            "trip_id": 97,
            "date_booked": "2025-05-01T18:04:19.193Z"
        },
        {
            "user_id": 101,
            "trip_id": 2,
            "date_booked": "2025-05-01T18:04:19.193Z"
        }
    ]
    for link in new_trip_links:
        user_trip_link.create(db_session, json.dumps(link))

    rec = main.recommend_trip(user_id=101)

    assert rec["trip_id"]
    # only this assertion needed; as long as what is returned
    # is a valid trip object (equivalent to it having a trip_id)
    # then things are good. it's difficult to test the quality of the recommendation
    # system; this might happen through user reviews when the api goes into production






