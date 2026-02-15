import json
import os
from datetime import datetime, timedelta, timezone

from ics import Calendar, Event


COUNTRY = {
    "US": "🇺🇸",
    "JP": "🇯🇵",
    "CN": "🇨🇳",
    "EU": "🇪🇺",
}

VOLATILITY ={
    "LOW":"🟢",
    "MEDIUM":"🟡",
    "HIGH":"🔴",
}


def build_description(ev: dict, config:dict) -> str:
    lines = []

    category_id = ev.get("categoryId", "").upper()
    category = [item for item in config["categories"] if item.get("id") == category_id]
    if len(category) > 0:
        lines.append(f"Category: {category[0]["name"]}")
    else:
        raise("find new category: "+category_id)

    if ev.get("isSpeech"):
        if ev["speech"]["isVotingMember"]:
            lines.append(f"票委-{ev["speech"]["averageScore"]}")

    return "\n".join(lines)


def load_events_for_country(country: str, base_dir: str = "event") -> list[dict]:
    country_dir = os.path.join(base_dir, country)
    if not os.path.exists(country_dir):
        return []

    events = []
    for month_dir in sorted(os.listdir(country_dir)):
        month_path = os.path.join(country_dir, month_dir)
        if not os.path.isdir(month_path):
            continue
        for day_file in sorted(os.listdir(month_path)):
            day_path = os.path.join(month_path, day_file)
            if not os.path.isfile(day_path):
                continue
            with open(day_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    events.extend(data)
                except json.JSONDecodeError:
                    continue
    return events


def generate_ics(config: dict, base_dir: str = "event", out_dir: str = "ics") -> None:
    os.makedirs(out_dir, exist_ok=True)

    for country in config["countries"]:
        events = load_events_for_country(country, base_dir)
        if not events:
            print(f"No events found for {country}, skipping")
            continue

        cal = Calendar()
        for ev in events:
            e = Event()
            e.uid = ev["id"]
            
            category_id = ev.get("categoryId", "").upper()
            category = [item for item in config["categories"] if item.get("id") == category_id]
            emoji = ''
            if len(category) > 0:
                emoji = f"{category[0]["emoji"]}"
            else:
                raise("find new category: "+category_id)
                
            volatility = ev.get("volatility", "")
    
            e.name = f"{COUNTRY.get(ev.get('countryCode', ''),'')}{emoji}-{VOLATILITY.get(volatility,'')}-{ev["name"]}"

            date_utc = ev["dateUtc"]
            dt = datetime.fromisoformat(date_utc.replace("Z", "+00:00"))

            if ev.get("isAllDay"):
                e.begin = dt.date()
                e.make_all_day()
            else:
                e.begin = dt
                e.end = dt + timedelta(hours=1)

            e.description = build_description(ev, config)
            cal.events.add(e)

        ics_path = os.path.join(out_dir, f"{country}.ics")
        with open(ics_path, "w", newline="") as f:
            f.write(cal.serialize())

        print(f"Generated {ics_path} with {len(events)} events")
