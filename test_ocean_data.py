from services.ocean_data_service import get_ocean_dataset
from services.ocean_data_service import analyze_ocean_conditions
from services.marine_risk_service import assess_marine_risk
from agents.gemini_agent import explain_marine_conditions
from services.ai_gateway import get_marine_explanation
print("Connecting to Copernicus Marine...")

ocean_data = get_ocean_dataset(
    latitude=13.08,
    longitude=80.27,
    start_time="2026-11-17T00:00:00",
    end_time="2026-11-17T01:00:00"
)

print("\nOcean data retrieved successfully!")

print("\nDataset information:")
print(ocean_data)

print("\nAvailable measurements:")
print(list(ocean_data.data_vars))

print("\nDataset dimensions:")
print(ocean_data.dims)
print("\nORCA Ocean Analysis:")

conditions = analyze_ocean_conditions(ocean_data)

for name, value in conditions.items():
    print(f"{name}: {value}")
    print("\nORCA Marine Risk Assessment:")

risk_result = assess_marine_risk(conditions)

print("Risk Level:", risk_result["risk_level"])

print("Risk Indicators:")
for risk in risk_result["risk_indicators"]:
    print("-", risk)

print("Disclaimer:", risk_result["disclaimer"])
print("\nORCA Gemini Marine Explanation:")

explanation = get_marine_explanation(
    conditions,
    risk_result
)

print("\nGemini Response:")
print(explanation)