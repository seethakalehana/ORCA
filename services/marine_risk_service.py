import math


def assess_marine_risk(ocean_conditions):

    temperature = ocean_conditions.get("temperature_c")
    current_speed = ocean_conditions.get("current_speed_m_s")
    sea_level = ocean_conditions.get("sea_surface_height_m")

    risks = []
    missing_data = []

    measurements = {
        "temperature": temperature,
        "current_speed": current_speed,
        "sea_surface_height": sea_level
    }

    for name, value in measurements.items():
        if value is None or not math.isfinite(value):
            missing_data.append(name)

    if missing_data:
        return {
            "risk_level": "Insufficient data for risk assessment",
            "risk_indicators": [],
            "missing_measurements": missing_data,
            "disclaimer": (
                "Missing measurements cannot be interpreted as safe conditions."
            )
        }

    if temperature >= 30:
        risks.append("High ocean temperature")

    if current_speed >= 1.0:
        risks.append("Strong ocean currents")

    if abs(sea_level) >= 1.0:
        risks.append("Unusual sea-surface height")

    if risks:
        risk_level = "Potential risk indicators detected"
    else:
        risk_level = "No risk indicators detected by these basic checks"

    return {
        "risk_level": risk_level,
        "risk_indicators": risks,
        "missing_measurements": [],
        "disclaimer": (
            "This is a preliminary screening, not a validated "
            "marine safety or navigation warning."
        )
    }