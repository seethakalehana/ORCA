
def assess_marine_risk(ocean_conditions):

    temperature = ocean_conditions["temperature_c"]
    current_speed = ocean_conditions["current_speed_m_s"]
    sea_level = ocean_conditions["sea_surface_height_m"]

    risks = []

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
        "disclaimer": (
            "This is a preliminary screening, not a validated "
            "marine safety or navigation warning."
        )
    }
