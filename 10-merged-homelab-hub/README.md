# 🏠 Project 10: Unified Homelab Hub & Media Automation

> **Centralized Media Server Operations Merging homepage, Flemmarr, docker-speedtest-analyser & Low-Latency Tweaks**

---

## 👤 Original Creators & Upstream Attribution
This mega-project stands on the shoulders of giants. We express our deepest respect and gratitude to the primary creators:
* **[@stevietv](https://github.com/stevietv)** (homepage, Flemmarr, docker-speedtest-analyser)
* **[@yuliskov](https://github.com/yuliskov)** (padavan-tweaks, windows-tweaks)

All foundational reverse engineering, API extraction, and protocols originated from their respective upstream repositories.

---

## 🚀 Why This Merged Version Is Better
- **Unified Control Plane:** Aggregates real-time health, active download queues, and media library status from Sonarr, Radarr, Prowlarr, and Plex into a single dashboard.
- **Declarative Configuration-as-Code:** Flemmarr YAML scripts allow entire media server configurations to be version-controlled and restored instantly with a single command.
- **Continuous Bandwidth & Latency Audits:** Headless speedtest recorder detects ISP throttling and latency degradation over time.
- **Network Stack Optimization:** Automated kernel and router TCP socket buffer tuning for stutter-free 4K video playback.

---

## 🚀 Quick Start

```bash
# Query unified homelab status:
python3 monitor.py
```
