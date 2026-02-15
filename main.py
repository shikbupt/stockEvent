import yaml

from src.fetch import fetch_events
from src.store import store_events
from src.generate_ics import generate_ics


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    print("=== Fetching events ===")
    events = fetch_events(config)

    print("=== Storing events ===")
    store_events(events)

    print("=== Generating ICS files ===")
    generate_ics(config)

    print("=== Done ===")


if __name__ == "__main__":
    main()
