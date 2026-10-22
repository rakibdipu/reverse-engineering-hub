# 📺 Project 08: OmniStream TV — The Ultimate Smart TV & Media Center

> **Unified Media Center Merging SmartTube, MediaServiceCore, LeanKeyboard & PlexTraktSync**

---

## 👤 Original Creators & Upstream Attribution
This mega-project stands on the shoulders of giants. We express our deepest respect and gratitude to the primary creators:
* **[@yuliskov](https://github.com/yuliskov)** (SmartTube, MediaServiceCore, LeanKeyboard)
* **[@stevietv](https://github.com/stevietv)** (PlexTraktSync, Sonarr, Radarr)

All foundational reverse engineering, API extraction, and protocols originated from their respective upstream repositories.

---

## 🚀 Why This Merged Version Is Better
- **Unified Interface:** Combines ad-free online streaming (YouTube 4K AV1 with SponsorBlock) and personal local media (Plex / Jellyfin) into a single Leanback TV interface.
- **Automated Trakt.tv Sync:** Seamlessly scrobbles playback progress and history to Trakt.tv whether watching personal media or online streams.
- **D-Pad Virtual Keyboard:** Embedded LeanKeyboard on-screen engine enables rapid directional remote typing without physical peripherals.
- **Headless & Cross-Platform:** Core streaming extraction is decoupled into a standalone Python runtime (`omnistream_core.py`) executable on Linux, Windows, macOS, or NAS servers.

---

## 🏗️ Architecture

```
       ┌────────────────────────────────────────────────────────┐
       │                   OmniStream TV UI                     │
       │     (Android Leanback UI + LeanKeyboard Integration)   │
       └───────────────────────────┬────────────────────────────┘
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
┌──────────────────┐                                ┌──────────────────┐
│  Online Stream   │                                │   Local Media    │
│ (MediaServiceCore│                                │  (Plex / Jellyfin│
│  + ExoPlayer)    │                                │  + TraktSync)    │
└────────┬─────────┘                                └────────┬─────────┘
         │                                                   │
         ▼                                                   ▼
┌──────────────────┐                                ┌──────────────────┐
│ PoTokenService   │                                │  Sonarr/Radarr   │
│ (Bypass 403 Bot) │                                │ (PVR Downloader) │
└──────────────────┘                                └──────────────────┘
```

---

## 🚀 Quick Start

```bash
# Run the standalone OmniStream TV core engine:
python3 omnistream_core.py
```
