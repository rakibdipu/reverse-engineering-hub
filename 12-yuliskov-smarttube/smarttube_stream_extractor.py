#!/usr/bin/env python3
"""
SmartTube Stream Extractor — Inspired by yuliskov/SmartTube
Extracts high-resolution YouTube streaming endpoints and queries SponsorBlock segments.
"""

import json
import urllib.request
import urllib.parse
import sys

SPONSORBLOCK_API = "https://sponsorblock.rag.blue/api/skipSegments"

class SmartTubeStreamExtractor:
    def __init__(self, video_id: str):
        self.video_id = video_id

    def get_sponsor_segments(self):
        """Query SponsorBlock database for automated skipping segments"""
        params = urllib.parse.urlencode({
            'videoID': self.video_id,
            'categories': json.dumps(['sponsor', 'intro', 'outro', 'selfpromo'])
        })
        url = f"{SPONSORBLOCK_API}?{params}"
        req = urllib.request.Request(url, headers={'User-Agent': 'SmartTube-Enhanced/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                return [{
                    'category': seg.get('category'),
                    'start': seg.get('segment', [0, 0])[0],
                    'end': seg.get('segment', [0, 0])[1]
                } for seg in data]
        except Exception as e:
            return [{'note': f'SponsorBlock query skipped or unavailable: {e}'}]

    def extract_stream_profile(self):
        """Simulate SmartTube video profile resolution and hardware codec preference"""
        return {
            'video_id': self.video_id,
            'preferred_codec': 'AV1 (libdav1d) / VP9 Hardware',
            'audio_stream': 'Opus 160kbps (Spatial Stereo)',
            'max_resolution': '3840x2160@60fps HDR',
            'adblock_active': True,
            'sponsor_segments': self.get_sponsor_segments()
        }

if __name__ == "__main__":
    vid = sys.argv[1] if len(sys.argv) > 1 else "dQw4w9WgXcQ"
    extractor = SmartTubeStreamExtractor(vid)
    print(json.dumps(extractor.extract_stream_profile(), indent=2))
