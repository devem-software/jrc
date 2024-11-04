import json
from datetime import datetime
from sre_constants import CATEGORY


def load_data(json_filename):
    with open(f"data/{json_filename}.json", "r", encoding="utf_8") as file:
        return json.load(file)


def save_readme(data, file_name):
    with open(file_name, "w", encoding="utf_8") as readme:
        readme.write(data)


def filter_data(data, key, value):
    filtered_games = [
        game
        for game in data["games"]
        if (
            game[key] == value.upper()
            if key != "teams"
            else value.upper() in game["teams"]
        )
    ]
    return {"games": filtered_games}


def generate_readme():
    return str


with open("data/partidos.json", "r", encoding="utf-8") as file:
    data = json.load(file)

print(
    len(
        [
            game["videoId"]
            for game in data["games"]
            if game["teams"][0] == "LOCAL" or game["teams"][1] == "VISITANTE"
        ]
    )
)


EQUIPO = "CHULOS"
CATEGORIA = "M"
MODALIDAD = "7"
AÑO = "2019"


data = load_data("partidos")
filtered = filter_data(data, "teams", EQUIPO)
filtered_male = filter_data(filtered, "category", CATEGORIA)
filtered_mod = filter_data(filtered_male, "modality", MODALIDAD)
filtered_year = filter_data(filtered_mod, "year", AÑO)

print(len(data["games"]), "JUEGOS")
print(len(filtered["games"]), f"JUEGOS {EQUIPO}")
print(len(filtered_male["games"]), f"JUEGOS {CATEGORIA} {EQUIPO}")
print(len(filtered_mod["games"]), f"JUEGOS {CATEGORIA} {EQUIPO} EN {MODALIDAD}'S")
print(
    len(filtered_year["games"]),
    f"JUEGOS {CATEGORIA} {EQUIPO} EN {MODALIDAD}'S DEL AÑO {AÑO}",
)

# print(data["games"])
# print("---------")
# print(filtered["games"])
# print("---------")
# print(filtered_male["games"])
# print("---------")
# print(filtered_mod["games"])
# print("---------")
# print(filtered_year["games"])
