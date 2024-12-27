from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.testclient import TestClient
from .database.database import Database

from .api import league_teams, points_per_position_per_week, test_db, points_on_bench, win_percentages

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the database
    db = Database()
    yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def get_root():
    return {"msg": "Hello World"}

@app.get('/teams')
async def get_teams():
    return league_teams()

@app.get('/points_per_position/{team_id}')
async def get_points_per_position(team_id):
    return points_per_position_per_week(team_id)

@app.get('/points_on_bench')
async def get_points_on_bench():
    return points_on_bench()

@app.get('/win_percentages')
async def get_win_percentages():
    return win_percentages()

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
