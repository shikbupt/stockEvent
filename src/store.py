import json
import os
from datetime import datetime, timezone


def store_events(events: list[dict], base_dir: str = "event") -> None:
    grouped: dict[str, dict[str, list[dict]]] = {}

    for event in events:
        country = event["countryCode"]
        date_utc = event["dateUtc"]
        dt = datetime.fromisoformat(date_utc.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d")
        month_str = dt.strftime("%Y-%m")

        grouped.setdefault(country, {}).setdefault(f"{month_str}/{date_str}", []).append(event)

    for country, date_map in grouped.items():
        for date_path, event_list in date_map.items():
            dir_path = os.path.join(base_dir, country, date_path.split("/")[0])
            os.makedirs(dir_path, exist_ok=True)

            file_path = os.path.join(base_dir, country, date_path)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(event_list, f, ensure_ascii=False, indent=2)

    print(f"Stored events for {len(grouped)} countries")
