
from services.inland_data_service import get_inland_conditions

result = get_inland_conditions(17.33, 78.61)

print("ORCA Inland Weather Data")
print("------------------------")
print(result)
