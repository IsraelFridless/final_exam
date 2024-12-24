from app.repository.mongo_repository.queries import *
from app.settings.mongo_config import events_collection


# Question No. 1
def get_deadliest_attack_type(limit=5) -> List[Dict]:
    pipeline = deadliest_attack_type_pipeline(limit=limit)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 2, Map introduction
def get_avg_casualty_score_per_region() -> List[Dict]:
    pipeline = avg_casualty_score_per_region_pipeline()
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 3
def get_groups_with_highest_casualty_score(limit: int = 5) -> List[Dict]:
    pipeline = highest_casualty_score_per_group_pipeline(limit=limit)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 7, Map introduction
def get_coordinates_by_date_range(start_year, start_month, end_year, end_month):
    if not (1 <= start_month <= 12 and 1 <= end_month <= 12):
        raise ValueError("Month should be between 1 and 12")
    pipeline = coordinates_by_date_range_pipeline(start_year, start_month, end_year, end_month)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 8, Map introduction
def get_most_active_groups_per_location(location_type: str = 'region', limit: int =5) -> List[Dict]:
    if location_type not in ['region', 'country', 'city']:
        raise ValueError("location_type must be either 'region' or 'country'.")
    pipeline = most_active_groups_per_location_pipeline(location_type, limit)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 11, Map introduction
def get_groups_by_location_and_mutual_targets(location_type: str = 'region') -> List[Dict]:
    if location_type not in ['region', 'country']:
        raise ValueError("location_type must be either 'region' or 'country'.")
    pipeline = groups_by_location_and_mutual_targets_pipeline(location_type)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 13
def get_multiple_groups_involved_in_event() -> List[Dict]:
    pipeline = multiple_groups_involved_in_event_pipeline()
    return list(events_collection.aggregate(pipeline))

# Question No. 14, Map introduction
def get_groups_by_attack_type_and_location(location_type: str = 'region') -> List[Dict]:
    if location_type not in ['region', 'country']:
        raise ValueError("location_type must be either 'region' or 'country'.")
    pipeline = groups_by_attack_type_and_location_pipeline(location_type)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 16, Map introduction
def get_coactive_groups_by_location(location_type: str = 'region') -> List[Dict]:
    if location_type not in ['region', 'country']:
        raise ValueError("location_type must be either 'region' or 'country'.")
    pipeline = coactive_groups_by_location_pipeline(location_type)
    result = list(events_collection.aggregate(pipeline))
    return result

# Question No. 17
def get_group_migration_patterns() -> List[Dict]:
    pipeline = group_migration_patterns_pipeline()
    result = list(events_collection.aggregate(pipeline))
    return result