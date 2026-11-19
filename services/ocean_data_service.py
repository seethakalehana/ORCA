from geopy.geocoders import Nominatim
import copernicusmarine


PRODUCT_ID = "GLOBAL_ANALYSISFORECAST_PHY_001_024"


def inspect_ocean_dataset():
    """Inspect Copernicus Marine dataset metadata."""

    print("Connecting to Copernicus Marine catalogue...")

    catalogue = copernicusmarine.describe(
        product_id=PRODUCT_ID,
        disable_progress_bar=True
    )

    if not catalogue.products:
        print("No product information found.")
        return

    product = catalogue.products[0]

    print("\nProduct:", product.title)
    print("\nAvailable datasets:")

    for dataset in product.datasets:
        print("\nDataset ID:", dataset.dataset_id)

        for version in dataset.versions:
            for part in version.parts:
                for service in part.services:
                    for variable in service.variables:
                        print(
                            "Variable:", variable.short_name,
                            "| Meaning:", variable.standard_name,
                            "| Unit:", variable.units
                        )


if __name__ == "__main__":
    inspect_ocean_dataset()
DATASET_ID = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m"

OCEAN_VARIABLES = ["thetao", "so", "uo", "vo", "zos"]


def get_ocean_dataset(latitude, longitude, start_time, end_time):

    ocean_data = copernicusmarine.open_dataset(
        dataset_id=DATASET_ID,
        variables=OCEAN_VARIABLES,
        minimum_longitude=longitude - 0.1,
        maximum_longitude=longitude + 0.1,
        minimum_latitude=latitude - 0.1,
        maximum_latitude=latitude + 0.1,
        start_datetime=start_time,
        end_datetime=end_time,
        coordinates_selection_method="nearest"
    )

    return ocean_data

def analyze_ocean_conditions(ocean_data):

    temperature = float(
        ocean_data["thetao"].mean(skipna=True).compute().item()
    )

    salinity = float(
        ocean_data["so"].mean(skipna=True).compute().item()
    )

    eastward_current = float(
        ocean_data["uo"].mean(skipna=True).compute().item()
    )

    northward_current = float(
        ocean_data["vo"].mean(skipna=True).compute().item()
    )

    sea_surface_height = float(
        ocean_data["zos"].mean(skipna=True).compute().item()
    )

    current_speed = float(
        (
            (ocean_data["uo"] ** 2 + ocean_data["vo"] ** 2) ** 0.5
        ).mean(skipna=True).compute().item()
    )

    return {
        "temperature_c": temperature,
        "salinity": salinity,
        "eastward_current_m_s": eastward_current,
        "northward_current_m_s": northward_current,
        "current_speed_m_s": current_speed,
        "sea_surface_height_m": sea_surface_height
    }

def geocode_location(city):
    geolocator = Nominatim(user_agent="orca_marine_assistant")
    location = geolocator.geocode(city)

    if location is None:
        raise ValueError(f"Could not find location: {city}")

    return location.latitude, location.longitude
