from datetime import datetime

from fastapi.testclient import TestClient
from ..controllers import user_trip_link as controller
from ..main import app
import pytest
from ..models import user_trip_link as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_user_trip_link(db_session):
    # Create sample user trip link data
    user_id = 71
    trip_id = 7101
    dummy_datetime = datetime(2025, 9, 20, 16, 10, 0)

    user_trip_link_data = {
        "user_id": user_id,
        "trip_id": trip_id,
        "date_booked": dummy_datetime,
    }

    # Create dummy user_trip_link object for testing
    user_trip_link_object = model.UserTripLink(**user_trip_link_data)

    # Call the create function
    created_link = controller.create(db_session, user_trip_link_object)

    # Assertions
    assert created_link is not None
    assert created_link.user_id == user_id
    assert created_link.trip_id == trip_id
    assert created_link.date_booked == dummy_datetime