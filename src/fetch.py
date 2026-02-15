from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import requests


API_BASE = "https://calendar-api.fxsstatic.com"
API_PATH = "/en/api/v2/eventDates"

HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Origin": "https://www.fxstreet.com",
    "Referer": "https://www.fxstreet.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/26.2 Safari/605.1.15"
    ),
}


def build_url(config: dict) -> str:
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=config["days_back"])
    end = now + timedelta(days=config["days_forward"])

    start_str = start.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_str = end.strftime("%Y-%m-%dT%H:%M:%SZ")

    params = []
    for v in config["volatilities"]:
        params.append(("volatilities", v))
    for c in config["countries"]:
        params.append(("countries", c))
    for cat in config["categories"]:
        params.append(("categories", cat["id"]))

    query = urlencode(params)
    return f"{API_BASE}{API_PATH}/{start_str}/{end_str}?{query}"


def fetch_events(config: dict) -> list[dict]:
    url = build_url(config)
    print(f"Fetching events from: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    print(f"Fetched {len(data)} events")
    return data
