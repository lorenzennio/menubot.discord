from datetime import date, time, datetime
from typing import Dict, List
import requests
import argparse


base_url = "https://tum-dev.github.io/eat-api/"
dish_types = {
    "Pasta": "🍝",
    "Pizza": "🍕",
    "Grill": "🍗",
    "Wok": "🍜",
    "Studitopf": "💸",
    "Vegetarisch": "🥕",
    "Vegetarisch/fleischlos": "🥕",
    "Vegan": "🥕",
    "Fleisch": "🥩",
    "Süßspeise": "🍭",
    "Fisch": "🐟",
    "Beilagen": "+",
}


def get_canteens() -> Dict:
    response = requests.get(f"{base_url}/enums/canteens.json")
    canteens = response.json()
    return {c["canteen_id"]: c for c in canteens}


def print_hours(canteen: str, canteens: dict):
    hours = canteens[canteen]["open_hours"]
    today = date.today().strftime("%A").lower()[:3]
    if today not in hours:
        print("\033[1;31mGeschlossen\033[0m")
        return

    start, end = hours[today]["start"], hours[today]["end"]
    if time.fromisoformat(start) < datetime.time(datetime.now()) < time.fromisoformat(end):
        status = "\033[1;32mOffen\033[0m"
    else:
        status = "\033[1;31mGeschlossen\033[0m"
    print(f"{status} (Öffnungszeiten {start} - {end})")


def print_occupancy(canteen: str):
    if canteen != "mensa-garching":
        return
    occupancy = requests.get("https://mensa.liste.party/api").json()
    percent = occupancy["percent"]
    queue = "▰"*int(percent/100 * 40) + "▱"*int(40 - percent/100*40)
    print(f"Wie voll ist es?  [{queue}] ({occupancy['current']})")


def get_week_menu(canteen: str, year: int, week_number: int) -> List[Dict]:
    response = requests.get(f"{base_url}/{canteen}/{year}/{week_number:02}.json")
    if response.status_code != 200:
        print(f"Error! {response.status_code}")
        return {}
    return response.json()["days"]


def get_today_menu(canteen: str) -> Dict:
    today = date.today()
    year, week, day = today.isocalendar()
    week_menu = get_week_menu(canteen, year, week)
    for menu in week_menu:
        if menu["date"] == today.isoformat():
            return menu
    return {}
        
def print_menu(menu: Dict):
    if not menu:
        return "Heut gibt's nix!"
    menu_str = ""
    for dish in menu["dishes"]:
        menu_str += f"{dish_types[dish['dish_type']]} {dish['name']} \n"
    return menu_str


def main(canteen: str, canteens: dict):
    print_hours(canteen, canteens)
    print_occupancy(canteen)
    print()
    menu = get_today_menu(canteen)
    print_menu(menu)


if __name__ == "__main__":
    canteens = get_canteens()

    parser = argparse.ArgumentParser(description="Was gibt's heut zu essen?")
    parser.add_argument(
        "-c",
        "--canteen",
        default="mensa-garching",
        choices=list(canteens.keys()),
        help="Wähle eine Mensa aus",
    )
    args = parser.parse_args()
    main(args.canteen, canteens)
