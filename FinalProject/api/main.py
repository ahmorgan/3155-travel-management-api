import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader, trips
from .dependencies.config import conf
from .dependencies.database import get_db
from sqlalchemy.orm import Session
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .controllers import trips, user_trip_link

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)


# Each trip is assigned two one-hot encoded vectors for trip location and category
# The index of the 1 in each array indicates the index for that trip location or category
def vectorize_trips(db, all_categories, all_locations):
    available_trips = trips.read_all(db)
    vectors = {}
    for trip in available_trips:
        trip = trip.as_dict()
        location_vec = np.zeros(len(all_locations))
        location_vec[all_locations.index(trip["country"])] = 1
        categories_vec = np.zeros(len(all_categories))
        categories_vec[all_categories.index(trip["category"])] = 1
        vectors.update({trip["trip_id"]: (location_vec, categories_vec)})
    return vectors


# Vectorize input trips into an average of one-hot encoded vectors, and do cosine similarity against all
# trips in the trip vector db to find the most similar trip (not including trips they've already been on)
def find_recommendation(trip_history, trip_vector_db, all_categories, all_locations):
    curr_ids = [trip["trip_id"] for trip in trip_history]

    avg_trip_vec = (np.array(np.zeros(len(all_locations))), np.array(np.zeros(len(all_categories))))
    loc_count = {loc: 0 for loc in all_locations}
    cat_count = {cat: 0 for cat in all_categories}
    for trip in trip_history:
        loc_count[trip["country"]] += 1
        cat_count[trip["category"]] += 1
    for i, loc in zip(range(len(avg_trip_vec[0])), all_locations):
        avg_trip_vec[0][i] = loc_count[loc] / len(all_locations)
    for j, cat in zip(range(len(avg_trip_vec[1])), all_categories):
        avg_trip_vec[1][j] = cat_count[cat] / len(all_categories)

    similarities = []
    for trip_id, (loc_vec, cat_vec) in trip_vector_db.items():
        loc_similarity = cosine_similarity([loc_vec], [avg_trip_vec[0]])
        cat_similarity = cosine_similarity([cat_vec], [avg_trip_vec[1]])
        similarity = (loc_similarity + cat_similarity) / 2
        if trip_id not in curr_ids:
            similarities.append((similarity, trip_id))

    recommendation = max(similarities)

    return recommendation[1]  # trip_id of recommended trip


# methodology: vector db approach: vectorize the user's trip history and the trip database, based on location and category
# define an index for each location and category in the list of all locations and categories
# create one-hot encoded vectors for each trip, ie, if India = index 3 and Nature = index 1, then the vectors for the trip
# (India, Nature) are [0,0,0,1, ... 0] and [0,1, ... 0]
# compute the argmax of the cosine similarity between the averaged trip vector (avg vectorized trip over all trips in user's history)
# and every vector in the trip vector database to find the most similar trip available
@app.get("/recommendation/{user_id}", tags=["Trip Recommendation"])
def recommend_trip(user_id: int, db: Session = Depends(get_db)):
    all_categories = trips.read_all_trip_categories(db)

    all_locations = trips.read_all_trip_locations(db)

    trip_vector_db = vectorize_trips(db, all_categories, all_locations)

    # Created new User controller that gets all of a user's trips
    trip_link_history = user_trip_link.read_all_user_trip_links(db, user_id=user_id)
    trip_history = []
    
    for trip_link in trip_link_history:
        trip_link = trip_link.as_dict()
        trip_history.append(trips.read_one(db, trip_link["trip_id"]).as_dict())

    # Based on trip location and category history, find the most similar trip
    recommendation_trip_id = find_recommendation(trip_history, trip_vector_db, all_categories, all_locations)
    recommendation = trips.read_one(db, item_id=recommendation_trip_id).as_dict()
    return recommendation


if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)