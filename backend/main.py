from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .database.database import Database

from .api import get_league_teams, get_points_per_position_per_week, test_db

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
    return test_db()

@app.get("/teams")
async def get_teams():
    return get_league_teams()

@app.get("/points_per_position/{team_id}")
async def get_points_per_position(team_id):
    return get_points_per_position_per_week(team_id)