from fastapi.testclient import TestClient
from ..controllers import user as controller
from ..main import app
import pytest
from ..models import user as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_user(db_session):
    # Create sample user data
    user_data = {
        "username": "testuser",
        "password": "test123"
    }

    # Create dummy user object for testing
    user_object = model.User(**user_data)

    # Call the create function
    created_user = controller.create(db_session, user_object)

    # Assertions
    assert created_user is not None
    assert created_user.username == "testuser"
    assert created_user.password == "test123"