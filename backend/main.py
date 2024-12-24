from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from decouple import config

from api import get_league_teams

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
def get_root():
    return {config('YEAR')}

@app.get("/teams")
def get_teams():
    return get_league_teams()

