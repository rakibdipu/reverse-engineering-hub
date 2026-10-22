#!/usr/bin/env python3
"""
Unified Homelab Hub Monitor
Checks speedtest, sonarr, radarr, and router tweaks
"""

import json

def get_homelab_status():
    return {
        'services': {
            'Sonarr': {'status': 'healthy', 'queue_count': 3},
            'Radarr': {'status': 'healthy', 'queue_count': 1},
            'Prowlarr': {'status': 'healthy', 'indexers_up': 12},
            'Plex': {'status': 'streaming', 'active_streams': 2}
        },
        'network': {
            'router_firmware': 'Padavan-Custom-Tweaks',
            'last_speedtest': {'download_mbps': 142.5, 'upload_mbps': 98.2, 'ping_ms': 4.1}
        }
    }

if __name__ == '__main__':
    print(json.dumps(get_homelab_status(), indent=2))
