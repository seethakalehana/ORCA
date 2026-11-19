
from datetime import datetime
from pydantic import BaseModel, model_validator
from services.ocean_data_service import (
    get_ocean_dataset,
    analyze_ocean_conditions,
    geocode_location
)
from services.marine_risk_service import assess_marine_risk
from services.ai_gateway import get_marine_explanation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.gemini_agent import answer_marine_question

app = FastAPI(
    title="ORCA - Marine Intelligence Assistant",
    description="AI-powered marine intelligence platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)


#class QuestionRequest(BaseModel):
   # question: str
    #city: str = "Chennai"
#class QuestionRequest(BaseModel):
   # question: str
# city: str = "Chennai"
   # start_time: str = "2026-11-17T00:00:00"
    #end_time: str = "2026-11-17T01:00:00"
class QuestionRequest(BaseModel):
    question: str
    city: str = "Chennai"
    start_time: datetime = "2026-11-17T00:00:00"
    end_time: datetime = "2026-11-17T01:00:00"

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self
@app.get("/")
def home():
    return {
        "message": "Welcome to ORCA Marine Intelligence Assistant",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask")
def ask_orca(request: QuestionRequest):

    latitude, longitude = geocode_location(request.city)

    ocean_data = get_ocean_dataset(
    latitude,
    longitude,
    request.start_time,
    request.end_time
)

    conditions = analyze_ocean_conditions(ocean_data)
    risk = assess_marine_risk(conditions)

    answer = answer_marine_question(
        request.question, conditions, risk
    )

    return {
        "city": request.city,
        "ocean_conditions": conditions,
        "risk_assessment": risk,
        "answer": answer
    }

@app.get("/marine-report")
def marine_report(
    latitude: float = 13.08,
    longitude: float = 80.27
):
    ocean_data = get_ocean_dataset(
        latitude,
        longitude,
        "2026-11-17T00:00:00",
        "2026-11-17T01:00:00"
    )

    conditions = analyze_ocean_conditions(ocean_data)
    risk = assess_marine_risk(conditions)

    explanation = get_marine_explanation(
        conditions, risk
    )

    return {
        "ocean_conditions": conditions,
        "risk_assessment": risk,
        "explanation": explanation
    }
