from app.settings.mongo_config import *


def get_central_coords_by_region(region: str):
    return region_collection.find_one(
        {"region": region},
        {"_id": 0, "region": 1, "latitude": 1, "longitude": 1}
    )

def get_central_coords_by_country(country: str):
    return country_collection.find_one(
        {"country": country},
        {"_id": 0, "region": 1, "latitude": 1, "longitude": 1}
    )