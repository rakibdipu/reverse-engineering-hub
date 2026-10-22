#!/usr/bin/env python3
"""
Homepage Service Widgets Exporter — Inspired by stevietv/homepage
"""

import json

def generate_widget_data():
    return {
        "services": [
            {"name": "Sonarr", "status": "online", "icon": "sonarr.png", "queue": 2},
            {"name": "Radarr", "status": "online", "icon": "radarr.png", "queue": 0},
            {"name": "Plex", "status": "streaming", "icon": "plex.png", "active_streams": 1},
            {"name": "qBittorrent", "status": "online", "icon": "qbittorrent.png", "download_rate": "12.4 MB/s"}
        ],
        "system": {
            "cpu_usage_pct": 14.2,
            "ram_used_gb": 6.8,
            "ram_total_gb": 16.0
        }
    }

if __name__ == "__main__":
    print(json.dumps(generate_widget_data(), indent=2))
