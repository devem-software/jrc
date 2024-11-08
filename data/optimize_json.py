import json
from datetime import datetime
from re import split


def set_path(file):
    return f"data/{file}"


def list2dict(items):
    return {item: index + 1 for index, item in enumerate(items)}


def load_file(filename):
    with open(set_path(f"{filename}.json"), "r", encoding="utf-8") as file:
        return list2dict(json.load(file)["data"])


def to_seconds(timestamp):

    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return int(dt.timestamp())


# para usar en javascript
# function toDateTime(unixSeconds) {
#     // Convertir segundos a milisegundos y crear un objeto Date
#     const date = new Date(unixSeconds * 1000);
#     return date.toISOString();
# }

# // Ejemplo de uso
# const unixSeconds = 1730326640; // resultado de la función en Python
# console.log(toDateTime(unixSeconds)); // Salida: "2024-10-30T21:57:20.000Z"


def duration(time):
    time = split(":", time)
    return (int(time[0]) * 60**2) + (int(time[1]) * 60**1) + (int(time[2]) * 60**0)


def optimize_partidos(origin, categories, modalities, teams, tournaments, years):

    with open(f"{set_path(origin)}.json", "r", encoding="utf-8") as origin_file:
        data = json.load(origin_file)
    print(len(data["games"]))

    categories_data = load_file(categories)
    teams_data = load_file(teams)
    femaleteams_data = load_file(f"female{teams}")
    maleteams_data = load_file(f"male{teams}")
    tournaments_data = load_file(tournaments)
    years_data = load_file(years)
    modalities_data = load_file(modalities)

    for game in data["games"]:
        game["addedAt"] = to_seconds(game["addedAt"])
        game["publishedAt"] = to_seconds(game["publishedAt"])
        game["duration"] = duration(game["duration"])
        game["year"] = years_data.get(game.get("year"), game.get("year"))
        game["modality"] = modalities_data.get(
            game.get("modality"), game.get("modality")
        )
        game["category"] = categories_data.get(
            game.get("category"), game.get("category")
        )
        game["tournament"] = tournaments_data.get(
            game.get("tournament"), game.get("tournament")
        )

        game["teams"] = [teams_data.get(team, team) for team in game.get("teams", [])]

    data["info"]["years"] = years_data
    data["info"]["modalities"] = modalities_data
    data["info"]["categories"] = categories_data
    data["info"]["tournaments"] = tournaments_data
    data["info"]["teams"] = teams_data
    data["info"]["femaleteams"] = femaleteams_data
    data["info"]["maleteams"] = maleteams_data

    with open(
        set_path(f"optimized_{origin}.json"), "w", encoding="utf-8"
    ) as destiny_file:
        json.dump(data, destiny_file, indent=1, ensure_ascii=False)

    return data


# Ejecutar la función de optimización
optimize_partidos(
    "partidos",
    "category",
    "modality",
    "teams",
    "tournament",
    "year",
)
