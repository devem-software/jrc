# from email import header
# import requests

# CHANNEL_ID = "UCgZ5IJNoVYleiAa4NT_F2qQ"
# API_KEY = "AIzaSyAb7pzBaJbrdmdGXeCTauI_fNA4bcMlh8M"
# CHANNEL_URL = f"https://youtube.com/channel/{CHANNEL_ID}"
# VIDEOS_FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

# req = requests.get(VIDEOS_FEED, headers={"User-Agent": "Chrome/100.0.0"})

# data = req.content

# print(data)
import json
import pandas as pd
from googleapiclient.discovery import build


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


import json


def save_videos_to_json(videos, filename="partidos_new.json"):
    with open(filename, "w") as json_file:
        json.dump(videos, json_file, indent=4)


# Uso
api_key = "AIzaSyAb7pzBaJbrdmdGXeCTauI_fNA4bcMlh8M"
channel_id = "UCgZ5IJNoVYleiAa4NT_F2qQ"
videos = get_youtube_videos(api_key, channel_id)

print(len(videos))

save_videos_to_json(videos)
