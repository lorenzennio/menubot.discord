from datetime import date
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
    "Fleisch": "🥩",
    "Süßspeise": "🍭",
    "Fisch": "🐟",
    "Beilagen": "+",
}
canteens = [
    "mensa-arcisstr",
    "mensa-garching",
    "mensa-leopoldstr",
    "mensa-lothstr",
    "mensa-martinsried",
    "mensa-pasing",
    "mensa-weihenstephan",
    "stubistro-arcisstr",
    "stubistro-goethestr",
    "stubistro-grosshadern",
    "stubistro-rosenheim",
    "stubistro-schellingstr",
    "stucafe-adalbertstr",
    "stucafe-akademie-weihenstephan",
    "stucafe-boltzmannstr",
    "stucafe-garching",
    "stucafe-karlstr",
    "stucafe-pasing",
    "ipp-bistro",
    "fmi-bistro",
    "mediziner-mensa",
]


def get_week_menu(canteen: str, year: int, week_number: int) -> List[Dict]:
    response = requests.get(f"{base_url}/{canteen}/{year}/{week_number}.json")
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


def main(canteen: str):
    menu = get_today_menu(canteen)
    return print_menu(menu)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Was gibt's heut zu essen?")
    parser.add_argument(
        "-c",
        "--canteen",
        default="mensa-garching",
        choices=canteens,
        help="Wähle eine Mensa aus",
    )
    args = parser.parse_args()
    main(args.canteen)
