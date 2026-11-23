import math
import numpy as np
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, model_validator
from services.inland_data_service import get_inland_conditions
from services.inland_risk_service import assess_inland_risk
from agents.gemini_agent import explain_inland_conditions
from services.ocean_data_service import (
    get_ocean_dataset,
    analyze_ocean_conditions,
    geocode_location
)
from services.marine_risk_service import assess_marine_risk
from services.ai_gateway import get_marine_explanation
from agents.gemini_agent import answer_marine_question


app = FastAPI(
    title="ORCA - Marine Intelligence Assistant",
    description="AI-powered marine intelligence platform",
    version="1.0.0"
)
def clean_nan_values(data):
    if isinstance(data, dict):
        return {
            key: clean_nan_values(value)
            for key, value in data.items()
        }

    if isinstance(data, (list, tuple)):
        return [clean_nan_values(value) for value in data]

    if isinstance(data, (float, np.floating)):
        if not math.isfinite(float(data)):
            return None

    if isinstance(data, np.integer):
        return int(data)

    return data
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://orca-1-67l3.onrender.com",
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QuestionRequest(BaseModel):
    question: str
    city: str = "Chennai"
    start_time: datetime = datetime(2026, 11, 17, 0, 0)
    end_time: datetime = datetime(2026, 11, 17, 1, 0)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self


def validate_coordinates(latitude: float, longitude: float):
    if not -90 <= latitude <= 90:
        raise HTTPException(400, "Latitude must be between -90 and 90.")

    if not -180 <= longitude <= 180:
        raise HTTPException(400, "Longitude must be between -180 and 180.")


@app.get("/")
def home():
    return {
        "message": "Welcome to ORCA Marine Intelligence Assistant",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/geocode")
def search_location(place: str):
    if not place.strip():
        raise HTTPException(400, "Please enter a location.")

    try:
        latitude, longitude = geocode_location(place.strip())

        validate_coordinates(latitude, longitude)

        return {
            "place": place,
            "latitude": latitude,
            "longitude": longitude
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=404,
            detail=f"Location could not be found: {str(error)}"
        )




@app.get("/marine-report")
def marine_report(latitude: float = 13.08, longitude: float = 80.27):
    validate_coordinates(latitude, longitude)

    try:
        ocean_data = get_ocean_dataset(
            latitude,
            longitude,
            "2026-11-17T00:00:00",
            "2026-11-17T01:00:00"
        )

        conditions = analyze_ocean_conditions(ocean_data)
        risk = assess_marine_risk(conditions)

        explanation = get_marine_explanation(conditions, risk)

        response_data = {
            "latitude": latitude,
            "longitude": longitude,
            "data_source": "Copernicus Marine",
            "ocean_conditions": conditions,
            "risk_assessment": risk,
            "explanation": explanation
        }

        return clean_nan_values(response_data)

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f"Marine data error: {str(error)}"
        )
@app.get("/inland-report")
def inland_report(
    latitude: float = 17.33,
    longitude: float = 78.61
):
    validate_coordinates(latitude, longitude)

    try:
        conditions = get_inland_conditions(latitude, longitude)
        risk = assess_inland_risk(conditions)

        explanation = explain_inland_conditions(
            conditions,
            risk
        )

        return {
            "location_type": "Inland",
            "data_source": "Open-Meteo",
            "weather_conditions": conditions,
            "risk_assessment": risk,
            "ai_explanation": explanation
        }

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f"Inland data error: {str(error)}"
        )

@app.post("/ask")
def ask_orca(request: QuestionRequest):
    try:
        latitude, longitude = geocode_location(request.city)

        ocean_data = get_ocean_dataset(
            latitude,
            longitude,
            request.start_time,
            request.end_time
        )

        conditions = analyze_ocean_conditions(ocean_data)
        conditions = clean_nan_values(conditions)

        risk = assess_marine_risk(conditions)
        explanation = explain_inland_conditions(
    conditions,
    risk
)
        answer = answer_marine_question(
            request.question,
            conditions,
            risk
        )

        return clean_nan_values({
            "city": request.city,
            "ocean_conditions": conditions,
            "risk_assessment": risk,
            "answer": answer,
            "ai_explanation": explanation
        })

    except Exception as error:
        raise HTTPException(
            status_code=422,
            detail=f"Unable to answer marine question: {str(error)}"
        )
