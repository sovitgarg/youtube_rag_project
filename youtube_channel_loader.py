# youtube_channel_loader.py
# ✅ Fetch videos from a YouTube channel
# ✅ Generate timestamped transcripts
# ✅ Store as JSON in data/transcripts/
# ✅ Support start-time-based playback URLs

import os
import requests
import json
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.discovery import build
import os

# ✅ Replace with your YouTube Data API key
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=youtube_api_key)

TRANSCRIPT_DIR = "data/transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def get_channel_video_ids(channel_id, max_videos=10):
    print(f"📺 Fetching videos for channel: {channel_id}")
    youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
    
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=max_videos,
        order="date",
        type="video"
    )
    
    response = request.execute()
    print("🔍 Raw YouTube API response:", response)

    video_ids = [
        item["id"]["videoId"]
        for item in response.get("items", [])
        if item["id"]["kind"] == "youtube#video"
    ]
    
    print("✅ Found video IDs:", video_ids)
    return video_ids




def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"No transcript found for {video_id}: {e}")
        return None


def save_transcript(video_id, transcript):
    filepath = os.path.join(TRANSCRIPT_DIR, f"{video_id}.json")
    with open(filepath, "w") as f:
        json.dump(transcript, f, indent=2)
    print(f"Saved: {filepath}")


def download_transcripts_from_channel(channel_id):
    video_ids = get_channel_video_ids(channel_id)
    for vid in video_ids:
        print(f"Fetching transcript for {vid}...")
        transcript = get_video_transcript(vid)
        if transcript:
            save_transcript(vid, transcript)


def get_youtube_url_with_start_time(video_id, start_time):
    return f"https://www.youtube.com/watch?v={video_id}&t={int(start_time)}s"


# ✅ Example usage:
# from youtube_channel_loader import download_transcripts_from_channel
# download_transcripts_from_channel("UCYO_jab_esuFRV4b17AJtAw")  # Example: 3Blue1Brown
