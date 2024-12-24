from typing import List, Dict


def avg_casualties_per_region_pipeline() -> List[Dict]:
    return [
        {
            "$project": {
                "region": "$location.region",
                "casualty_points": {
                    "$add": [
                        {"$multiply": ["$casualties.fatalities", 2]},
                        {"$multiply": ["$casualties.injuries", 1]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$region",
                "total_points": {"$sum": "$casualty_points"},
                "event_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "region": "$_id",
                "avg_casualty_points": {"$divide": ["$total_points", "$event_count"]},
                "_id": 0
            }
        }
    ]

def deadliest_attack_type_pipeline(limit: int) -> List[Dict]:
    return [
        {
            "$addFields": {
                "deadliness_score": {
                    "$add": [
                        {"$multiply": ["$casualties.fatalities", 2]},
                        "$casualties.injuries"
                    ]
                }
            }
        },
        {"$unwind": "$attack_types"},
        {
            "$match": {
                "$and": [
                    {"attack_types": {"$ne": None}},
                    {"attack_types": {"$ne": "Unknown"}}
                ]
            }
        },
        {
            "$group": {
                "_id": "$attack_types",
                "max_deadliness": {"$max": "$deadliness_score"}
            }
        },
        {"$sort": {"max_deadliness": -1}},
        {"$limit": limit},
        {
            "$project": {
                "_id": 0,
                "attack_type": "$_id",
                "max_deadliness": 1
            }
        }
    ]

def avg_casualty_score_per_region_pipeline() -> List[Dict]:
    return [{
        "$match": {
            "location.region": {"$exists": True, "$ne": None}
        }
        },
        {
            "$project": {
                "region": "$location.region",
                "casualtiesScore": {
                    "$add": [
                        {"$multiply": ["$casualties.fatalities", 2]},
                        "$casualties.injuries"
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$region",
                "avgCasualtyScore": {"$avg": "$casualtiesScore"}
            }
        },
        {
            "$project": {
                "region": "$_id",
                "avgCasualtyScore": 1,
                "_id": 0
            }
        },
        {
            "$sort": {"avgCasualtyScore": -1}
        }
    ]

def highest_casualty_score_per_group_pipeline(limit: int) -> List[Dict]:
    return [
        {
            "$match": {
                "groups_involved": {"$exists": True, "$ne": None, "$not": {"$size": 0}}
            }
        },
        {
            "$match": {
                "groups_involved": {"$nin": ["Unknown", None, "unknown", "Other", ""]}
            }
        },
        {
            "$project": {
                "groups_involved": 1,
                "casualtiesScore": {
                    "$add": [
                        {"$multiply": ["$casualties.fatalities", 2]},
                        "$casualties.injuries"
                    ]
                }
            }
        },
        {
            "$unwind": "$groups_involved"
        },
        {
            "$group": {
                "_id": "$groups_involved",
                "totalCasualtiesScore": {"$sum": "$casualtiesScore"}
            }
        },
        {
            "$sort": {"totalCasualtiesScore": -1}
        },
        {
            "$limit": limit
        },
        {
            "$project": {
                "group": "$_id",
                "totalCasualtiesScore": 1,
                "_id": 0
            }
        }
    ]

def coordinates_by_date_range_pipeline(start_year: int, start_month: int, end_year: int, end_month: int) -> List[Dict]:
    return [
        {
            "$match": {
                "date.year": { "$gte": start_year, "$lte": end_year },
                "date.month": { "$gte": start_month, "$lte": end_month }
            }
        },
        {
            "$project": {
                "_id": 0,
                "location": {
                    "$cond": {
                        "if": {
                            "$and": [
                                { "$ne": ["$location.latitude", None] },
                                { "$ne": ["$location.longitude", None] },
                                { "$ne": ["$location.latitude", float('nan')] },
                                { "$ne": ["$location.longitude", float('nan')] }
                            ]
                        },
                        "then": "$location",
                        "else": "$$REMOVE"
                    }
                },
                "timeframe": {
                    "$concat": [
                        { "$toString": "$date.year" },
                        "-",
                        { "$toString": "$date.month" },
                        "-",
                        { "$toString": "$date.day" }
                    ]
                }
            }
        }
    ]

def most_active_groups_per_location_pipeline(location_type: str, limit: int) -> List[Dict]:
    return [
        {"$unwind": "$groups_involved"},

        {
            "$match": {
                f"location.{location_type}": {"$nin": ["", "unknown", 'Unknown', None]},
                "groups_involved": {"$nin": ["", "unknown", 'Unknown', None]}
            }
        },
        {
            "$group": {
                "_id": {location_type: f"$location.{location_type}", "group": "$groups_involved"},
                "eventCount": {"$sum": 1}
            }
        },
        {
            "$sort": {f"_id.{location_type}": 1, "eventCount": -1}
        },
        {
            "$group": {
                "_id": f"$_id.{location_type}",
                "topGroups": {
                    "$push": {
                        "group": "$_id.group",
                        "eventCount": "$eventCount"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                location_type: "$_id",
                "topGroups": {"$slice": ["$topGroups", limit]},
                "countGroups": {"$literal": limit}
            }
        },
        {
            "$sort": {location_type: 1}
        }
    ]

def groups_by_location_and_mutual_targets_pipeline(location_type: str) -> List[Dict]:
    return [
        {"$unwind": "$groups_involved"},
        {"$unwind": "$target_types"},
        {
            "$match": {
                f"location.{location_type}": {"$nin": ["", "unknown", None]},
                "groups_involved": {"$nin": ["", "Unknown", None]}
            }
        },
        {
            "$group": {
                "_id": {
                    "target": "$target_types",
                    location_type: f"$location.{location_type}"
                },
                "groups": {"$addToSet": "$groups_involved"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "target": "$_id.target",
                location_type: f"$_id.{location_type}",
                "groups": 1,
                "groupCount": {"$size": "$groups"}
            }
        },
        {"$sort": {"groupCount": -1}},
        {
            "$group": {
                "_id": f"${location_type}",
                "target": {"$first": "$target"},
                "groups": {"$first": "$groups"},
                "groupCount": {"$first": "$groupCount"}
            }
        },
        {
            "$project": {
                "_id": 0,
                location_type: "$_id",
                "target": 1,
                "groups": 1,
                "groupCount": 1
            }
        },
        {"$sort": {location_type: 1}}
    ]

def groups_by_attack_type_and_location_pipeline(location_type: str) -> List[Dict]:
    return [
        {"$unwind": "$groups_involved"},
        {"$unwind": "$attack_types"},
        {
            "$match": {
                f"location.{location_type}": {"$nin": ["", "Unknown", None]}
            }
        },
        {
            "$group": {
                "_id": {
                    location_type: f"$location.{location_type}",
                    "attack_type": "$attack_types"
                },
                "groups": {"$addToSet": "$groups_involved"}
            }
        },
        {
            "$project": {
                "_id": 0,
                location_type: f"$_id.{location_type}",
                "attack_type": "$_id.attack_type",
                "groups": 1,
                "groupCount": {"$size": "$groups"}
            }
        },
        {"$sort": {"groupCount": -1}},
        {
            "$group": {
                "_id": f"${location_type}",
                "attack_type": {"$first": "$attack_type"},
                "groups": {"$first": "$groups"},
                "groupCount": {"$first": "$groupCount"}
            }
        },
        {
            "$project": {
                "_id": 0,
                location_type: "$_id",
                "attack_type": 1,
                "groups": 1,
                "groupCount": 1
            }
        },
        {"$sort": {location_type: 1}}
    ]

def coactive_groups_by_location_pipeline(location_type: str) -> List[Dict]:
    return [
        {"$unwind": "$groups_involved"},
        {
            "$match": {
                f"location.{location_type}": {"$nin": ["", "Unknown", None]}
            }
        },
        {
            "$group": {
                "_id": f"$location.{location_type}",
                "unique_groups": {"$addToSet": "$groups_involved"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "region": "$_id",
                "unique_groups": 1,
                "countGroups": {"$size": "$unique_groups"}
            }
        },
        {"$sort": {"region": 1}}
    ]

def multiple_groups_involved_in_event_pipeline() -> List[Dict]:
    return [
        {
            "$match": {
                "groups_involved": {"$exists": True, "$not": {"$size": 1}}
            }
        },
        {
            "$project": {
                "groups_involved": 1
            }
        },
        {
            "$unwind": "$groups_involved"
        },
        {
            "$group": {
                "_id": None,
                "all_groups": {"$addToSet": "$groups_involved"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "all_groups": 1,
                "count_groups": {"$size": "$all_groups"}
            }
        }
    ]

def group_migration_patterns_pipeline() -> List[Dict]:
    return [
        {
            "$match": {
                "location": {"$exists": True},
                "date": {"$exists": True},
                "location.region": {"$nin": [None, 'Unknown']},
                "location.country": {"$nin": [None, 'Unknown']},
                "location.city": {"$nin": [None, 'Unknown']},
                "groups_involved": {"$exists": True, "$nin": [None, 'Unknown', []]}
            }
        },
        {
            "$addFields": {
                "date": {
                    "$dateFromParts": {
                        "year": "$date.year",
                        "month": "$date.month",
                        "day": "$date.day"
                    }
                }
            }
        },
        {
            "$addFields": {
                "year": {"$year": "$date"},
                "month": {"$month": "$date"}
            }
        },
        {
            "$group": {
                "_id": {
                    "region": "$location.region",
                    "country": "$location.country",
                    "city": "$location.city",
                    "group": {"$arrayElemAt": ["$groups_involved", 0]},
                    "year": "$year",
                    "month": "$month"
                },
                "total_events": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id.year": 1, "_id.month": 1}
        },
        {
            "$project": {
                "region": "$_id.region",
                "country": "$_id.country",
                "city": "$_id.city",
                "group": "$_id.group",
                "year": "$_id.year",
                "month": "$_id.month",
                "total_events": 1
            }
        }
    ]