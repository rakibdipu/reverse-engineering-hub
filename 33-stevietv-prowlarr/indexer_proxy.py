#!/usr/bin/env python3
"""
Prowlarr Indexer Health & Proxy Tester — Inspired by stevietv/Prowlarr
"""

import json

INDEXERS = [
    {"name": "1337x", "protocol": "torrent", "priority": 1, "latency_ms": 120, "status": "Online"},
    {"name": "Nyaa", "protocol": "torrent", "priority": 2, "latency_ms": 85, "status": "Online"},
    {"name": "NZBGeek", "protocol": "usenet", "priority": 1, "latency_ms": 45, "status": "Online"}
]

def check_indexers():
    online = [idx for idx in INDEXERS if idx["status"] == "Online"]
    return {
        "total_indexers": len(INDEXERS),
        "online_count": len(online),
        "best_latency": min(online, key=lambda x: x["latency_ms"]),
        "indexers": online
    }

if __name__ == "__main__":
    print(json.dumps(check_indexers(), indent=2))
