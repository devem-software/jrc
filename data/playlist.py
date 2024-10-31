import json
from multiprocessing.reduction import duplicate
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

api_key = os.getenv("YOUTUBE_API_KEY")
channel_id = os.getenv("YOUTUBE_CHANNEL_ID")


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
            print(item, details)
            video_data = {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                # "description": item["snippet"]["description"],
                "publishedAt": item["snippet"]["publishedAt"],
                "duration": details["contentDetails"]["duration"],
            }
            videos.append(video_data)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos


def save_videos_to_json(videos, filename="partidos_new.json"):
    with open(filename, "w") as json_file:
        json.dump(videos, json_file, indent=4)


# videos = get_youtube_videos(api_key, channel_id)

# print(len(videos))

# save_videos_to_json(videos)

from collections import Counter

with open("data/partidos.json", "r", encoding="utf_8") as file:
    data = json.load(file)

ids = [item["videoId"] for item in data["games"]]
idsCount = Counter(ids)

duplicates = [id for id, count in idsCount.items() if count > 1]

print(duplicates)
print(len(data["games"]))
