#!/usr/bin/env python3
"""
Plex Subtitle Preference Automation — Inspired by stevietv/PlexPreferNonForcedSubs
"""

import json

def process_stream_preferences(streams: list, preferred_lang="eng"):
    selected_sub = None
    for s in streams:
        if s.get("type") == "subtitle" and s.get("language_code") == preferred_lang:
            if not s.get("forced", False):
                selected_sub = s
                break
    return {
        "preferred_language": preferred_lang,
        "selected_track": selected_sub or "Default",
        "action": "Set active subtitle track in Plex DB"
    }

if __name__ == "__main__":
    sample_streams = [
        {"type": "subtitle", "language_code": "eng", "forced": True},
        {"type": "subtitle", "language_code": "eng", "forced": False, "title": "English Full"}
    ]
    print(json.dumps(process_stream_preferences(sample_streams), indent=2))
