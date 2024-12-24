from typing import List
from dataclasses import dataclass

from app.models.casualties import Casualties
from app.models.date import Date
from app.models.location import Location

@dataclass
class Event:
    date: Date
    location: Location
    perpetrators: int
    groups_involved: List[str]
    attack_types: List[str]
    target_types: List[str]
    casualties: Casualties
    summary: str