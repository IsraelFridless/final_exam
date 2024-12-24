from dataclasses import dataclass

@dataclass
class Location:
    region: str
    country: str
    city: str
    latitude: float
    longitude: float