import os
import json

TRANSCRIPT_DIR = "data/transcripts"

def get_all_transcript_chunks():
    chunks = []
    for filename in os.listdir(TRANSCRIPT_DIR):
        if filename.endswith(".json"):
            video_id = filename.replace(".json", "")
            with open(os.path.join(TRANSCRIPT_DIR, filename), "r") as f:
                data = json.load(f)
                for entry in data:
                    chunks.append({
                        "text": entry["text"],
                        "start": entry["start"],
                        "end": entry["start"] + entry.get("duration", 0),  # ✅ safely compute end
                        "video_id": video_id
                    })
    return chunks

