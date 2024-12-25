from typing import Dict, List, Optional
import toolz as t

from app.api.groq_api import classify_and_extract_location
from app.service.geopy_coords_convertion import get_coords
from app.repository.article_repository import insert_articles


def extract_article_fields(article: Dict) -> Dict:
    fields_to_extract = ["dateTime", "url", "title", "body"]
    return {field: article.get(field) for field in fields_to_extract}

def merge_coords(article_dict: Dict) -> Optional[Dict]:
    return t.pipe(
        article_dict.get('location_info'),
        get_coords,
        t.partial(lambda coords, orig: {**orig, **coords}, orig=article_dict)
    ) if article_dict else None

def process_article(article: Dict):
    return t.pipe(
        article,
        extract_article_fields,
        classify_and_extract_location,
        merge_coords,
    )

def process_batch_and_insert_articles(articles: List[Dict]):
    return t.pipe(
        articles,
        t.partial(map, process_article),
        list,
        insert_articles
    )