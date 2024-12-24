from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_log, after_log
import json
import requests
from groq import Groq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = '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'
groq_client = Groq(api_key=GROQ_API_KEY)

VALID_REGIONS = [
    'Central America & Caribbean', 'North America', 'Southeast Asia',
    'Western Europe', 'East Asia', 'South America', 'Eastern Europe',
    'Sub-Saharan Africa', 'Middle East & North Africa', 'Australasia & Oceania',
    'South Asia', 'Central Asia'
]

VALID_CATEGORIES = ['current_terror_event', 'historical_terror_event', 'general_news']

def create_prompt(content_json: str) -> str:
    return (
        f"'{content_json}  \n\n"
        "return a json result based on the structure provided below:\n"
        "\"region\":\n}\n"
        "\"country\": ,\n"
        "\"city\": ,\n"
        "\"category\": ,\n"
        f"\"the region should be in this list of regions: {VALID_REGIONS}\n"
        f"\"the region should be in this list of regions: {VALID_REGIONS}\n"
        f"the category field should be in this list: {VALID_CATEGORIES}\n"
        "please only send the json without any other text content\n"
    )

def get_groq_completion(messages: list, **kwargs) -> str:
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
        **kwargs
    )

    result = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            result += chunk.choices[0].delta.content

    return result.strip()

def parse_location_response(result: str) -> Optional[dict]:
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON response. The raw response was: %s", result)
        return None

def extract_location_info(result_json: dict) -> dict:
    return {
        "location_info": {
            "region": result_json.get("region"),
            "country": result_json.get("country"),
            "city": result_json.get("city"),
        },
        "category": result_json.get('category')
    }

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.exceptions.RequestException, TimeoutError)),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.INFO),
)
def classify_and_extract_location(content: dict) -> Optional[dict]:
    try:
        content_json = json.dumps(content, ensure_ascii=False)

        messages = [{"role": "user", "content": create_prompt(content_json)}]

        result = get_groq_completion(messages)
        logger.info(f"Raw response from Groq API: {result}")

        result_json = parse_location_response(result)
        if result_json is None:
            return None

        location_data = extract_location_info(result_json)
        return {**content, **location_data}

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise