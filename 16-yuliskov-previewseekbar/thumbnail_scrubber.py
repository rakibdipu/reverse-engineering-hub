#!/usr/bin/env python3
"""
PreviewSeekBar Engine — Inspired by yuliskov/PreviewSeekBar
Parses video sprite sheets for real-time scrub preview thumbnails.
"""

import json

class ThumbnailScrubber:
    def __init__(self, sprite_cols=5, sprite_rows=5, interval_seconds=10, thumb_w=160, thumb_h=90):
        self.cols = sprite_cols
        self.rows = sprite_rows
        self.interval = interval_seconds
        self.w = thumb_w
        self.h = thumb_h
        self.thumbs_per_sheet = sprite_cols * sprite_rows

    def get_thumbnail_coords(self, playback_second: float):
        index = int(playback_second // self.interval)
        sheet_index = index // self.thumbs_per_sheet
        local_index = index % self.thumbs_per_sheet

        col = local_index % self.cols
        row = local_index // self.cols

        return {
            "playback_time_s": playback_second,
            "sheet_file": f"storyboard_sheet_{sheet_index:03d}.jpg",
            "x": col * self.w,
            "y": row * self.h,
            "width": self.w,
            "height": self.h
        }

if __name__ == "__main__":
    scrubber = ThumbnailScrubber()
    for sec in [15, 65, 320]:
        print(f"Scrub to {sec}s ->", json.dumps(scrubber.get_thumbnail_coords(sec)))
