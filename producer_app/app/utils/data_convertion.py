import math

import pandas as pd
from typing import Dict, List, Optional
from app.models.casualties import Casualties
from app.models.date import Date
from app.models.event import Event
from app.models.location import Location


def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def nullable_float(value: str) -> Optional[float]:
    return float(value) if value not in [None, ""] else None

def validate_numeric_field(value: Optional[float]) -> Optional[float]:
    if pd.isnull(value) or value <= 0:
        return None
    return value

def validate_coordinates(latitude, longitude):
    if math.isnan(latitude) or math.isnan(longitude):
        return True
    if not (-90 <= latitude <= 90):
        raise ValueError(f"Invalid latitude value: {latitude}")
    if not (-180 <= longitude <= 180):
        raise ValueError(f"Invalid longitude value: {longitude}")
    return True

def extract_non_empty_values(csv_row: Dict, count: int, explicit_fields: List[str] = None, field_name: str = None) -> List[str]:
    def is_real_value(value):
        return value and not (isinstance(value, float) and math.isnan(value))

    if explicit_fields:
        return [
            str(csv_row.get(field, "")).strip()
            for field in explicit_fields
            if is_real_value(csv_row.get(field, ""))
        ]
    else:
        return [
            str(csv_row.get(f"{field_name}{i}_txt", "")).strip()
            for i in range(1, count + 1)
            if is_real_value(csv_row.get(f"{field_name}{i}_txt", ""))
        ]

def extract_string_value(value) -> Optional[str]:
    if isinstance(value, float) and math.isnan(value):
        return None
    return value if isinstance(value, str) else None

def extract_event_from_row(csv_row: Dict):
    date = Date(
        year=int(csv_row.get("iyear")) or None,
        month=int(csv_row.get("imonth")) or None,
        day=int(csv_row.get("iday")) or None,
    )

    latitude = nullable_float(csv_row.get("latitude"))
    longitude = nullable_float(csv_row.get("longitude"))

    if latitude is not None and longitude is not None:
        try:
            validate_coordinates(latitude, longitude)
        except ValueError as e:
            print(f"Error in coordinates: {e}")
            latitude, longitude = None, None

    location = Location(
        region=extract_string_value(csv_row.get("region_txt")),
        country = extract_string_value(csv_row.get("country_txt")),
        city = extract_string_value(csv_row.get("city")),
        latitude=latitude,
        longitude=longitude,
    )

    try:
        fatalities = int(validate_numeric_field(pd.to_numeric(csv_row.get("nkill"), errors='coerce')))
        injuries = int(validate_numeric_field(pd.to_numeric(csv_row.get("nwound"), errors='coerce')))

        casualties = Casualties(
            fatalities=fatalities or 0,
            injuries=injuries or 0
        )
    except (ValueError, TypeError):
        casualties = Casualties(fatalities=0, injuries=0)

    perpetrators_value = pd.to_numeric(csv_row.get("nperps"), errors='coerce')
    perpetrators = int(perpetrators_value) if pd.notnull(perpetrators_value) and perpetrators_value > 0 else None

    return Event(
        date=date,
        location=location,
        perpetrators=perpetrators,
        groups_involved=extract_non_empty_values(csv_row, count=0, explicit_fields=["gname", "gname2"]),
        attack_types=extract_non_empty_values(csv_row, field_name="attacktype", count=2),
        target_types=extract_non_empty_values(csv_row, field_name="targtype", count=3),
        casualties=casualties,
        summary=extract_string_value(csv_row.get("summary"))
    )