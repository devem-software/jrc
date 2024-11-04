import json
import re

partidos = []


def load_json(filename):
    with open(filename, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
    return data


partidos = load_json("partidos.json")

for idx, video in enumerate(partidos, start=1):
    # Extraer los equipos del título
    title = video["title"]
    equipos = [team.strip() for team in title.split("vs")]

    match = re.search(r"(\w+)\s+vs\s+(\w+)", video["title"], re.IGNORECASE)
    if match:
        equipos = [match.group(1), match.group(2)]  # Primer equipo y segundo equipo
    else:
        equipos = ["N/A", "N/A"]  # Por si no hay un "vs"

    # Crear la estructura del partido
    partido = {
        "id": idx,  # Auto incremental
        "yt_id": video["videoId"],
        "date": video["publishedAt"],
        "dur": video["duration"],
        "teams": equipos,
    }

    print(partido["teams"])

    partidos.append(partido)

# print(partidos)
