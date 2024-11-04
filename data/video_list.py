import json
import re
import pandas as pd


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data


def format_duration(iso_duration):
    # Expresión regular para capturar horas, minutos y segundos
    pattern = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")
    match = pattern.match(iso_duration)

    hours = match.group(1) if match.group(1) else "00"
    minutes = match.group(2) if match.group(2) else "00"
    seconds = match.group(3) if match.group(3) else "00"

    # Asegurar formato de dos dígitos
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    seconds = seconds.zfill(2)

    # Retornar la duración en el formato "HH:MM:SS"
    return f"{hours}:{minutes}:{seconds}"


def reformat_json_durations(filename):
    # Cargar el archivo JSON
    with open(filename, "r") as json_file:
        videos = json.load(json_file)

    # Reformatear la duración en cada entrada
    for video in videos:
        video["duration"] = format_duration(video["duration"])

    # Guardar los cambios en el mismo archivo o en uno nuevo
    with open(filename, "w") as json_file:
        json.dump(videos, json_file, indent=4)


# Ejemplo de uso con un archivo que contiene los 500 JSON


def add_fields(filename):
    with open(filename, "r", encoding="utf8") as file:
        data = json.load(file)

        for video in data:
            video["year"] = ""
            video["teams"] = ["LOCAL", "VISITANTE"]
            video["tournament"] = ""
            video["category"] = ""
            video["modality"] = ""
            video["events"] = [
                {
                    "scrums": [],
                    "lineouts": [],
                    "ruck": [],
                    "amonestaciones": {
                        "fouls": [],
                        "tarjetas": {"roja": [], "amarilla": []},
                    },
                    "anotaciones": {
                        "try": [],
                        "conversion": [],
                        "drop": [],
                        "penal": [],
                    },
                },
                {
                    "scrums": [],
                    "lineouts": [],
                    "ruck": [],
                    "amonestaciones": {
                        "fouls": [],
                        "tarjetas": {"roja": [], "amarilla": []},
                    },
                    "anotaciones": {
                        "try": [],
                        "conversion": [],
                        "drop": [],
                        "penal": [],
                    },
                },
            ]

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    return data


def add_games(games, teams):
    with open(games, "r", encoding="utf-8") as g:
        data_games = json.load(g)
    with open(teams, "r", encoding="utf-8") as t:
        data_teams = json.load(t)

    for video in data_games:
        id = video["videoId"]
        for game in data_teams:
            if game[0] == id:
                video["teams"] = [game[1], game[2]]
        # return None
        print(video)

    with open(games, "w") as file:
        json.dump(data_games, file, indent=4)


# json_data = load_json("partidos.json")
# reformat_json_durations("partidos.json")
# print(add_fields("partidos.json"))
# add_games("partidos.json", "teams.json")


def add_year(filename):
    with open(filename, "r", encoding="utf-8") as file:
        games = json.load(file)

    for game in games:
        game["year"] = game["publishedAt"].split("-")[0]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(games, file, indent=4)


# add_year("partidos.json")


def view_data(filename, item):
    result = []

    with open(filename, "r", encoding="utf-8") as file:
        games = json.load(file)["games"]

    for game in games:
        if game[item] == "":
            result.append([game["videoId"], game["title"]])

    print(result)


# view_data("partidos.json", "year")


def view_teams(filename):
    with open(filename, "r", encoding="utf-8") as file:
        games = json.load(file)

    teams = set()

    for game in games:
        teams.add(game[1])
        teams.add(game[2])

    teams_list = list(teams)

    print(sorted(teams_list))


# view_teams("teams.json")


def view_item(filename, item):
    with open(filename, "r", encoding="utf-8") as file:
        games = json.load(file)["games"]

    items = set()

    for game in games:
        items.add(game[item])

    items_list = list(items)

    return sorted(items_list)


# data = view_item("partidos.json", "modality")
# print(pd.DataFrame(data).to_string())


def view_filter(file, item, value):
    with open(file, "r", encoding="utf-8") as f:
        games = json.load(f)["games"]

    data_filter = [game for game in games if game[item] == value]

    return data_filter


def view_team_filter(file):
    with open(file, "r", encoding="utf-8") as f:
        games = json.load(f)["games"]

    data_filter = [
        game for game in games if game["teams"][0] == "A" or game["teams"] == "B"
    ]

    return data_filter


# data = view_team_filter("partidos.json")
# print(pd.DataFrame(data)["videoId"].to_string())
# data = view_filter("partidos.json", "modality", "")
# print(pd.DataFrame(data)["title"].to_string())


def data_filter(file, item_find, reg, item_update, data_update):

    with open(file, "r", encoding="utf-8") as f:
        games = json.load(f)

    for game in games["games"]:
        if any(key in game[item_find] for key in reg):
            game[item_update] = data_update

    # print(games)

    with open(file, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4)


view = "category"
reg: list[str] = ["12's Masculino"]
update = "M"

# print(pd.DataFrame(view_item("partidos.json", view)).to_string())
data_filter("data/partidos.json", "title", reg, view, update)
print(pd.DataFrame(view_filter("data/partidos.json", view, ""))["videoId"].to_string())
