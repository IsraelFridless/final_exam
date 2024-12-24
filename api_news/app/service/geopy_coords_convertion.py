from typing import Dict

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="my_final_exam_project", timeout=10)

def get_coords(location: Dict[str, str]) -> Dict[str, float]:
    location_str = ', '.join(
        filter(None, [location.get('city'), location.get('country')])
    )
    try:
        result = geolocator.geocode(location_str, timeout=None)
        if result:
            res = {"latitude": result.latitude, "longitude": result.longitude}
            return res
        else:
            print(f"No geocoding result found for '{location_str}'")
            return {}
    except Exception as e:
        print(f"Geocoding error: {e}")
        return {}

