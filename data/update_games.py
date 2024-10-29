import json
import re
from datetime import datetime


def format_duration(iso_duration):
    # Expresión regular para capturar horas, minutos y segundos
    pattern = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")
    match = pattern.match(iso_duration)

    hours = match.group(1) if match.group(1) else "00"  # type: ignore
    minutes = match.group(2) if match.group(2) else "00"  # type: ignore
    seconds = match.group(3) if match.group(3) else "00"  # type: ignore

    # Asegurar formato de dos dígitos
    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    seconds = seconds.zfill(2)

    # Retornar la duración en el formato "HH:MM:SS"
    return f"{hours}:{minutes}:{seconds}"


def add_games(filename):
    with open(f"{filename}.json", "r", encoding="utf8") as file:
        data = json.load(file)
    with open(f"{filename}_new.json", "r", encoding="utf8") as new_file:
        new_data = json.load(new_file)

    existing_video_ids = {video["videoId"] for video in data["games"]}

    last_video_update = max(
        datetime.strptime(video["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        for video in new_data
    )

    for video in new_data:
        if video["videoId"] not in existing_video_ids:
            new_video = {
                "videoId": video["videoId"],
                "title": video["title"],
                "publishedAt": video["publishedAt"],
                "duration": format_duration(video["duration"]),
                "year": video["publishedAt"].split("-")[0],
                "teams": ["A", "B"],
                "score": [0, 0],
                "tournament": "",
                "category": "",
                "modality": "",
                "events": [
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
                ],
            }
            data["info"]["period"] = [
                max(int(video["year"]) for video in games),
                min(int(video["year"]) for video in games),
            ]
            data["info"]["last_update"] = str(last_video_update)
            data["games"].append(new_video)

    # with open(f"{filename}.json", "w") as file:
    # json.dump(data, file, indent=4)

    return data


games = add_games("partidos")["games"]

print(
    [
        max(int(video["year"]) for video in games),
        min(int(video["year"]) for video in games),
    ]
)
