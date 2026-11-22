
def assess_inland_risk(conditions):
    weather = conditions.get("current_conditions", {})

    precipitation = weather.get("precipitation")
    wind_speed = weather.get("wind_speed_10m")
    temperature = weather.get("temperature_2m")

    indicators = []

    if precipitation is not None and precipitation >= 10:
        indicators.append("Heavy precipitation detected")

    if wind_speed is not None and wind_speed >= 40:
        indicators.append("Strong wind conditions detected")

    if temperature is not None and temperature >= 40:
        indicators.append("High temperature detected")

    if indicators:
        risk_level = "Potential weather risk indicators detected"
    else:
        risk_level = "No risk indicators detected by these basic checks"

    return {
        "risk_level": risk_level,
        "risk_indicators": indicators,
        "disclaimer": (
            "This is a preliminary weather screening, "
            "not an official weather warning."
        )
    }
