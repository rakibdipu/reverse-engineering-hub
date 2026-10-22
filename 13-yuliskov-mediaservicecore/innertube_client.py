#!/usr/bin/env python3
"""
InnerTube Client Engine — Inspired by yuliskov/MediaServiceCore
Direct communication with YouTube InnerTube backend without Google API keys.
"""

import urllib.request
import json

class InnerTubeClient:
    INNERTUBE_URL = "https://www.youtube.com/youtubei/v1/player"

    def __init__(self, client_name="TVHTML5", client_version="7.20230405.08.01"):
        self.client_name = client_name
        self.client_version = client_version

    def build_context(self):
        return {
            "client": {
                "clientName": self.client_name,
                "clientVersion": self.client_version,
                "hl": "en",
                "gl": "US"
            }
        }

    def fetch_player_metadata(self, video_id: str):
        payload = json.dumps({
            "context": self.build_context(),
            "videoId": video_id
        }).encode("utf-8")

        req = urllib.request.Request(
            self.INNERTUBE_URL,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (SMART-TV; Linux; Tizen 5.0)"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
                details = data.get("videoDetails", {})
                return {
                    "title": details.get("title", "Unknown"),
                    "author": details.get("author", "Unknown"),
                    "length_seconds": details.get("lengthSeconds", 0),
                    "view_count": details.get("viewCount", 0),
                    "is_live": details.get("isLiveContent", False)
                }
        except Exception as e:
            return {"error": str(e), "hint": "Run with valid network or verify videoId"}

if __name__ == "__main__":
    client = InnerTubeClient()
    print("Testing InnerTube endpoint extraction:")
    print(json.dumps(client.fetch_player_metadata("jNQXAC9IVRw"), indent=2))
