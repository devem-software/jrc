import json
import re
import os
from googleapiclient.discovery import build
from datetime import datetime

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

def format_duration(iso_duration):
    pattern = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")
    match = pattern.match(iso_duration)
    hours = match.group(1) if match.group(1) else "00"
    minutes = match.group(2) if match.group(2) else "00"
    seconds = match.group(3) if match.group(3) else "00"

    hours = hours.zfill(2)
    minutes = minutes.zfill(2)
    seconds = seconds.zfill(2)

    return f"{hours}:{minutes}:{seconds}"


def get_youtube_videos(api_key, channel_id):
    youtube = build("youtube", "v3", developerKey=api_key)

    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=1200,
            pageToken=next_page_token,
            type="video",
        )
        response = request.execute()

        video_ids = [item["id"]["videoId"] for item in response["items"]]
        video_details = (
            youtube.videos()
            .list(part="contentDetails", id=",".join(video_ids))
            .execute()
        )

        for item, details in zip(response["items"], video_details["items"]):
            video_data = {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "publishedAt": item["snippet"]["publishedAt"],
                "duration": details["contentDetails"]["duration"],
            }
            videos.append(video_data)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos

def save_videos_to_json(videos, filename="partidos"):
    with open(f"data/{filename}.json", "w") as json_file:
        json.dump(videos, json_file, indent=4)

def add_games(filename="partidos"):
    with open(f"data/{filename}.json", "r", encoding="utf8") as file:
        data = json.load(file)
    with open(f"data/{filename}_new.json", "r", encoding="utf8") as new_file:
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
                max(int(video["year"]) for video in data["games"]),
                min(int(video["year"]) for video in data["games"]),
            ]
            data["info"]["last_update"] = str(last_video_update)
            data["games"].append(new_video)

    with open(f"{filename}.json", "w") as file:
    json.dump(data, file, indent=4)

    return data

filename ="partidos"
videos = get_youtube_videos(
  YOUTUBE_API_KEY, 
  YOUTUBE_CHANNEL_ID
  )

save_videos_to_json(videos, f"{filename}_new" )
add_games(filename)