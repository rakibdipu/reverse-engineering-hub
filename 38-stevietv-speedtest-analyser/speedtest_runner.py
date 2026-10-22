#!/usr/bin/env python3
"""
Headless Speedtest Monitor — Inspired by stevietv/docker-speedtest-analyser
"""

import time
import json

def run_speedtest_sample():
    # Simulated speedtest result
    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ping_ms": 8.4,
        "download_mbps": 185.2,
        "upload_mbps": 94.6,
        "isp": "Broadband Fiber",
        "status": "Optimal"
    }

if __name__ == "__main__":
    print(json.dumps(run_speedtest_sample(), indent=2))
