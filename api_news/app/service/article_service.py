from typing import Dict
import toolz as t

from app.api.groq_api import classify_and_extract_location
from app.service.geopy_coords_convertion import get_coords
from app.repository.article_repository import insert_articles


def extract_article_fields(article: Dict) -> Dict:
    fields_to_extract = ["dateTime", "url", "title", "body"]
    return {field: article.get(field) for field in fields_to_extract}

def merge_coords(article_dict):
    coords = get_coords(article_dict.get('location_info'))
    return {**article_dict, **coords}

def process_articles_batch(article: Dict):
    return t.pipe(
        article,
        extract_article_fields,
        classify_and_extract_location,
        merge_coords,
        lambda x: insert_articles([x])
    )