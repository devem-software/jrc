from enum import unique
import json
import os
import re
from collections import Counter

if os.name == "nt":
    # Limpiar consola en windows
    os.system("cls")
else:
    # Limpiar consola en Unix/Linux/Mac
    os.system("clear")


def load_data(path):
    with open(path) as file:
        return json.load(file)


def save_items(item, origin, destiny):
    with open(origin) as origin_file:
        data = json.load(origin_file)["games"]

    unique_items = set()

    for video in data:
        modality = video.get(item)
        if modality:
            unique_items.add(modality)

    # Ordena los valores numéricos primero, luego los valores de cadena alfabéticamente
    ordered_list = sorted(
        unique_items, key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x)
    )

    with open(destiny, "w", encoding="utf-8") as destiny_file:
        json.dump(
            {"title": item, "count": len(ordered_list), "data": ordered_list},
            destiny_file,
            indent=2,
        )


def save_teams(origin, destiny):
    with open(origin) as origin_file:
        data = json.load(origin_file)["games"]

    unique_teams = set()
    for video in data:
        unique_teams.update(video.get("teams", []))

    order_list = sorted(list(unique_teams))

    with open(destiny, "w", encoding="utf-8") as destiny_file:
        json.dump(
            {"title": "teams", "count": len(order_list), "data": order_list},
            destiny_file,
            indent=4,
        )


save_teams("data/partidos.json", "data/teams.json")
save_items("category", "data/partidos.json", "data/category.json")
save_items("modality", "data/partidos.json", "data/modality.json")
save_items("tournament", "data/partidos.json", "data/tournament.json")
save_items("year", "data/partidos.json", "data/year.json")


def find_duplicates(data):
    ids = [video["videoId"] for video in data]
    id_count = Counter(ids)

    ids_duplicados = {id for id, count in id_count.items() if count > 1}

    registers = [item for item in data if item["videoId"] in ids_duplicados]
    return {
        "count": len(registers),
        "data": list(set(game["videoId"] for game in registers)),
    }


def filter_videos_under_10_minutes(data):
    # Expresión regular para tiempos menores a 10 minutos
    regex = r"^00:0[0-9]:[0-5][0-9]$"
    # Filtrar los videos que cumplen el patrón
    registers = [video for video in data if re.match(regex, video["duration"])]

    return {
        "conut": len(registers),
        "data": list(set(register["videoId"] for register in registers)),
    }


def filter_by(data, key, value):
    filtered = [video["videoId"] for video in data if video[key] == value]
    return {"count": len(filtered), "data": filtered}


def filter_by_teams(data):
    filtered = [video["videoId"] for video in data if video.get("teams") == ["A", "B"]]
    return {"count": len(filtered), "data": filtered}


data = load_data("data/partidos.json")


# Imprimir registros duplicados
print("Registros duplicados")
print(find_duplicates(data["games"]))
print("")
# Imprimir registros menores a 10 minutos
print("Registros menores a 10 minutos")
print(filter_videos_under_10_minutes(data["games"]))
print("")
# Imprimir registros sin categoria
print("Registros sin categoria")
print(filter_by(data["games"], "category", ""))
print("")
# Imprimir registros sin modalidad
print("Registros sin modalidad")
print(filter_by(data["games"], "modality", ""))
print("")
# Imprimir registros sin modalidad
print("Registros sin torneo")
print(filter_by(data["games"], "tournament", ""))
print("")
# Imprimir registros sin modalidad
print("Registros sin equipos")
print(filter_by_teams(data["games"]))
print("")
