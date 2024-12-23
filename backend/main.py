from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from decouple import config

from api import get_league_teams, get_points_per_position_per_week

app = FastAPI()

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
    return {config('YEAR')}

@app.get("/teams")
async def get_teams():
    return get_league_teams()

@app.get("/points_per_position/{team_id}")
async def get_points_per_position(team_id):
    return get_points_per_position_per_week(team_id)