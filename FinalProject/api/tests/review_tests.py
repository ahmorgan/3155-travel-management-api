from datetime import datetime
from fastapi.testclient import TestClient
from ..controllers import review as controller
from ..main import app
import pytest
from ..models import review as model
from ..models import user_trip_link as link_model
from ..schemas import review as schema

# Create a test client for the app
client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_review(db_session):
    # Create sample review data
    user_id = 1
    trip_id = 71
    rating = 5
    comment = "Excellent trip!"
    review_data = schema.ReviewCreate(
        user_id=user_id,
        trip_id=trip_id,
        rating=rating,
        comment=comment
    )

    # Mock the UserTripLink confirmation query
    mock_user_trip_link = link_model.UserTripLink(user_id=user_id, trip_id=trip_id)
    db_session.query.return_value.filter.return_value.first.return_value = mock_user_trip_link

    # Call the create function
    created_review = controller.create(db_session, review_data)

    # Assertions
    assert created_review is not None
    assert created_review.user_id == user_id
    assert created_review.trip_id == trip_id
    assert created_review.rating == rating
    assert created_review.comment == comment

def test_read_all_reviews(db_session):
    # Query to return a list of review objects
    mock_reviews = [
        model.Review(review_id=1, user_id=1, trip_id=10, rating=5, comment="Great!"),
        model.Review(review_id=2, user_id=2, trip_id=20, rating=4, comment="Good."),
    ]
    db_session.query.return_value.all.return_value = mock_reviews

    # Call the read_all function
    all_reviews = controller.read_all(db_session)

    # Assertions
    assert all_reviews is not None
    assert len(all_reviews) == 2
    assert all_reviews[0].review_id == 1
    assert all_reviews[1].review_id == 2

def test_read_review(db_session):
    # Sample review ID to read
    review_id_to_read = 1

    # Query to return a specific review
    mock_review = model.Review(review_id=review_id_to_read, user_id=1, trip_id=10, rating=5, comment="Great!")
    db_session.query.return_value.filter.return_value.first.return_value = mock_review

    # Call the read_one function
    read_review_result = controller.read_one(db_session, review_id_to_read)

    # Assertions
    assert read_review_result is not None
    assert read_review_result.review_id == review_id_to_read
    assert read_review_result.user_id == 1
    assert read_review_result.trip_id == 10
    assert read_review_result.rating == 5
    assert read_review_result.comment == "Great!"

def test_update_review(db_session):
    # Sample review ID to update
    review_id_to_update = 3

    # Create sample updated data
    updated_rating = 4
    updated_comment = "Good trip!"
    updated_data = schema.ReviewUpdate(
        rating=updated_rating,
        comment=updated_comment
    )

    # Query for the review to be updated
    mock_review_to_update = model.Review(
        review_id=review_id_to_update,
        user_id=1,
        trip_id=1,
        rating=updated_rating,
        comment=updated_comment)

    db_session.query.return_value.filter.return_value.first.return_value = mock_review_to_update

    # Call the update function
    updated_review_response = controller.update(db_session, review_id_to_update, updated_data)

    # Assertions
    assert updated_review_response is not None
    assert updated_review_response.rating == updated_rating
    assert updated_review_response.comment == updated_comment

def test_delete_review(db_session):
    # Sample review ID to delete
    review_id_to_delete = 2
    user_id = 1
    trip_id = 1
    rating = 5
    comment = "deletable"

    mock_review_to_delete = model.Review(
        review_id=review_id_to_delete,
        user_id=user_id,
        trip_id=trip_id,
        rating=rating,
        comment=comment)

    # Query for review to be deleted.
    db_session.query.return_value.filter.return_value.first.return_value = mock_review_to_delete


    # Call the delete function
    deleted_review_response = controller.delete(db_session, review_id_to_delete)

    # Assertions
    assert deleted_review_response.status_code == 204