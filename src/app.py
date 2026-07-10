"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}

# Additional activities
activities.update({
    "Soccer Club": {
        "description": "Outdoor soccer practices and intramural matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Skills, drills, and friendly games",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["sophia@mergington.edu", "mason@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting, stagecraft, and school productions",
        "schedule": "Mondays, 4:30 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Club": {
        "description": "Drawing, painting, and mixed media workshops",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Math Olympiad": {
        "description": "Problem solving and preparation for competitions",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Experiments, projects, and science fairs",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["oliver@mergington.edu", "amelia@mergington.edu"]
    }
})


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


class SignupRequest(BaseModel):
    email: EmailStr


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, payload: SignupRequest):
    """Sign up a student for an activity using a JSON body with an email."""
    # Normalize activity lookup (allow exact name matching only)
    if activity_name not in activities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")

    activity = activities[activity_name]

    # Validate student is not already signed up
    if payload.email in activity["participants"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Student is already signed up for this activity")

    # Validate capacity
    if len(activity.get("participants", [])) >= activity.get("max_participants", 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Activity is full")

    # Add student
    activity.setdefault("participants", []).append(payload.email)
    return {"message": f"Signed up {payload.email} for {activity_name}"}


@app.get("/activities/{activity_name}")
def get_activity(activity_name: str):
    if activity_name not in activities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
    return activities[activity_name]
