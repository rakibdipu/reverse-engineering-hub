# 🔬 Reverse Engineering & Automation Mega Hub

> **AI-Assisted Reverse Engineering, Open-Source Creative Software Alternatives, Android TV Streaming Ecosystem & Low-Level OS Internals**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()
[![Projects](https://img.shields.io/badge/Projects-50%2B-blue)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Rust](https://img.shields.io/badge/Rust-2021%20Edition-orange.svg)](https://www.rust-lang.org/)

---

## 📸 Live Repository Preview

![GitHub Repository Preview](screenshots/github_repo.png)

---

## 📋 Overview

The **Reverse Engineering & Automation Mega Hub** is an extensive, production-grade monorepo containing over **50 modular projects** and **4 unified mega-platforms** spanning binary reverse engineering, low-level OS internals, Android TV media engines, and clean-room Rust implementations of creative desktop software.

This repository curates, improves upon, and merges groundbreaking research from world-class reverse engineers: **[@yuliskov](https://github.com/yuliskov)**, **[@WitherOrNot](https://github.com/WitherOrNot)**, **[@stevietv](https://github.com/stevietv)**, **[@storytold](https://github.com/storytold)**, and **[@morluto](https://github.com/morluto)**.

---

## 🌟 Upstream Creators Hall of Fame & Full Attribution

Every module in this repository stands on the shoulders of giants. We express our deepest gratitude and provide complete upstream attribution to the pioneering developers:

| Creator & Profile | Key Innovations & Upstream Repos | Our Enhancements & Merged Value |
|---|---|---|
| **[@yuliskov (Yuriy L)](https://github.com/yuliskov)** | [SmartTube](https://github.com/yuliskov/SmartTube), [MediaServiceCore](https://github.com/yuliskov/MediaServiceCore), [LeanKeyboard](https://github.com/yuliskov/LeanKeyboard), [PoTokenService](https://github.com/yuliskov/PoTokenService) | Decoupled Android SDK dependencies into standalone cross-platform Python engines; merged ad-free streaming with local Plex synchronization into `OmniStream TV`. |
| **[@WitherOrNot](https://github.com/WitherOrNot)** | [XenonRecomp-XEO3](https://github.com/WitherOrNot/XenonRecomp-XEO3), [StartXBack](https://github.com/WitherOrNot/StartXBack), [warbird-docs](https://github.com/WitherOrNot/warbird-docs), [cbsexploder](https://github.com/WitherOrNot/cbsexploder), [uupget](https://github.com/WitherOrNot/uupget), [mpclient](https://github.com/WitherOrNot/mpclient) | Synthesized fragmented utilities (Play Store APK fetching, Windows UUP updates, Defender mpengine) into an automated, headless `Zero-API App Pipeline`. |
| **[@stevietv](https://github.com/stevietv)** | [PlexTraktSync](https://github.com/stevietv/PlexTraktSync), [Sonarr](https://github.com/stevietv/Sonarr), [Radarr](https://github.com/stevietv/Radarr), [Flemmarr](https://github.com/stevietv/Flemmarr), [homepage](https://github.com/stevietv/homepage) | Merged *arr media automation, declarative configuration-as-code, bandwidth monitoring, and router QoS tuning into the `Unified Homelab Hub`. |
| **[@storytold](https://github.com/storytold)** | [PhotoCraft](https://github.com/storytold/photocraft), [VectorCraft](https://github.com/storytold/vectorcraft), [FilmCraft](https://github.com/storytold/filmcraft), [LightCraft](https://github.com/storytold/lightcraft), [EffectCraft](https://github.com/storytold/effectcraft) | Documented binary proprietary formats (PSD, AI, PRPROJ, LRCAT, AEP) and provided complete runnable desktop GUI implementations in pure Rust (`eframe`/`egui`). |
| **[@morluto](https://github.com/morluto)** | [REA Tool](https://github.com/morluto/rea) (Reverse Engineer Anything) | Developed a standalone Python Model Context Protocol (MCP) server directly bridging Claude Code and Cursor with headless Ghidra and IDA Pro disassemblers. |

---

## 🗂️ Repository Structure

```
reverse-engineering-hub/
│
├── 📁 01-07: REVERSE ENGINEERING & CREATIVE SUITE
│   ├── 01-REA-tool/                    # REA: Reverse Engineer Anything (AI + Ghidra + IDA MCP Server)
│   ├── 02-photoshop-alternative/       # PhotoCraft — Photoshop Alternative (PSD Binary RE + Rust egui)
│   ├── 03-illustrator-alternative/     # VectorCraft — Illustrator Alternative (Bezier Engine + SVG/AI)
│   ├── 04-premiere-alternative/        # FilmCraft — Premiere Pro Alternative (PRPROJ RE + NLE Timeline)
│   ├── 05-lightroom-alternative/       # LightCraft — Lightroom Alternative (LRCAT SQLite RE + RAW Engine)
│   ├── 06-aftereffects-alternative/    # EffectCraft — After Effects Alternative (AEP RIFX RE + WGSL Shader)
│   └── 07-ps5-jailbreak-research/      # PS5 Console Firmware Security & AI-Accelerated Exploit Analysis
│
├── 📁 08-11: UNIFIED MERGED MEGA-PROJECTS
│   ├── 08-merged-omnistream-tv/        # OmniStream TV (SmartTube + InnerTube + Plex + Trakt Sync)
│   ├── 09-merged-app-pipeline/         # Zero-API Headless App Pipeline (gplayapi + uupget + mpclient)
│   ├── 10-merged-homelab-hub/          # Unified Homelab Hub (homepage + Flemmarr + Speedtest Monitor)
│   └── 11-merged-remote-gaming-input/  # Virtual Remote Gaming Controller (chunithm + LeanKeyboard + QEMU)
│
├── 📁 12-18: ANDROID TV & STREAMING ECOSYSTEM (yuliskov)
│   ├── 12-yuliskov-smarttube/          # SmartTube & SmartTubeLegacy (4K HDR, AV1/VP9, SponsorBlock)
│   ├── 13-yuliskov-mediaservicecore/   # InnerTube API Extractor & Signature Decipher Engine
│   ├── 14-yuliskov-leankeyboard/       # Android TV D-Pad Remote On-Screen Keyboard Engine
│   ├── 15-yuliskov-potokenservice/     # YouTube Proof of Origin (PO) Bot Bypass Token Generator
│   ├── 16-yuliskov-previewseekbar/     # Video Scrubbing Thumbnail Preview Sprite Sheet Parser
│   ├── 17-yuliskov-chat-suite/         # Asynchronous WebSocket Real-Time Chat Server & JWT Auth
│   └── 18-yuliskov-system-tweaks/      # Low-Latency TCP Streaming & Network Buffer Optimization
│
├── 📁 19-31: OS INTERNALS, RE & EMULATION (WitherOrNot)
│   ├── 19-witherornot-xenonrecomp-xeo3/# Xbox 360 PPC Static Recompiler ABI Bridge for XEO3
│   ├── 20-witherornot-startxback/      # In-Memory Shell Hook & Trampoline Injection Scanner
│   ├── 21-witherornot-musedash-dlc-unlock/ # Unity Harmony Dynamic IL Instruction Patcher
│   ├── 22-witherornot-warbird-docs/    # Microsoft Warbird Code Encryption & Entropy Scanner
│   ├── 23-witherornot-cbsexploder-sxsfounder/ # Windows CBS (.mum) Update Manifest & WinSxS Parser
│   ├── 24-witherornot-uupget/          # Microsoft Unified Update Platform Direct Catalog Client
│   ├── 25-witherornot-winkeycheck-licensing/ # Windows 5x5 Product Key Decoder & Digital License Research
│   ├── 26-witherornot-ohook/           # Universal SPP COM VTable Hook & DLL Proxy Interceptor
│   ├── 27-witherornot-mpclient/        # Standalone Microsoft Defender mpengine.dll CLI Wrapper
│   ├── 28-witherornot-gplayapi/        # Headless Google Play Store API Client & APK Resolver
│   ├── 29-witherornot-qemui/           # Modern QEMU Virtual Machine Configuration & Runner
│   ├── 30-witherornot-ntfstool/        # NTFS Master File Table ($MFT) Record Forensics Parser
│   └── 31-witherornot-console-hacks/   # Nintendo Switch Tegra RCM Coldboot Payload Builder
│
├── 📁 32-39: HOMELAB & MEDIA AUTOMATION (stevietv)
│   ├── 32-stevietv-sonarr-radarr/      # Unified Sonarr & Radarr Media Automation API Client
│   ├── 33-stevietv-prowlarr/           # Torznab & Newznab Indexer Aggregator & Latency Monitor
│   ├── 34-stevietv-flemmarr/           # Declarative Configuration-as-Code Sync Engine for *arr
│   ├── 35-stevietv-plektraktsync/      # Local Plex Media Server to Trakt.tv Two-Way Scrobbler
│   ├── 36-stevietv-plex-subs/          # Batch Subtitle Language Preference Automation Engine
│   ├── 37-stevietv-homepage-dashboard/ # Real-time Docker & Homelab Metrics Exporter for Homepage
│   ├── 38-stevietv-speedtest-analyser/ # Headless Network Speedtest Monitor & Trend Logger
│   └── 39-stevietv-vehicle-telematics/ # Hyundai Bluelink & Kia UVO Telematics API Client
│
└── 📁 docs/
    ├── REFERENCES.md                   # Curated Reference Papers, Articles & Libraries
    └── TOP_50_PROJECTS_CATALOG.md      # Comprehensive Catalog Table of All 50 Repositories
```

---

## ⚡ The 4 Unified Merged Mega-Projects

Instead of keeping valuable utilities siloed, we engineered 4 unified platforms that combine multiple upstream components:

### 1. 📺 OmniStream TV (`08-merged-omnistream-tv`)
* **Components Merged:** `yuliskov/SmartTube` + `yuliskov/MediaServiceCore` + `yuliskov/LeanKeyboard` + `stevietv/PlexTraktSync`
* **Innovation:** An all-in-one smart media center that unifies online streaming (YouTube 4K AV1 with SponsorBlock) and local personal media (Plex/Jellyfin) into a single Leanback TV interface, complete with D-pad typing and bidirectional Trakt.tv watch history scrobbling.

### 2. ⚡ Zero-API App & Media Pipeline (`09-merged-app-pipeline`)
* **Components Merged:** `WitherOrNot/gplayapi` + `WitherOrNot/uupget` + `WitherOrNot/mpclient` + `yuliskov/PoTokenService`
* **Innovation:** An end-to-end automated asset pipeline that downloads original Google Play APKs, fetches genuine Windows ESD/CAB update packages directly from Microsoft servers, bypasses stream bot-detection throttles via PO tokens, and instantly audits all binaries using the native Microsoft Defender scanning engine.

### 3. 🏠 Unified Homelab Hub (`10-merged-homelab-hub`)
* **Components Merged:** `stevietv/homepage` + `stevietv/Flemmarr` + `stevietv/docker-speedtest-analyser` + `yuliskov/padavan-tweaks`
* **Innovation:** Centralized homelab control plane combining a unified service health dashboard, declarative configuration-as-code for all media apps, automated bandwidth tracking, and router TCP buffer optimizations for high-bitrate 4K streaming.

### 4. 🎮 Virtual Remote Gaming Controller (`11-merged-remote-gaming-input`)
* **Components Merged:** `WitherOrNot/chunithm-vcontroller` + `WitherOrNot/qemui` + `yuliskov/LeanKeyboard`
* **Innovation:** Cross-device input bridge translating mobile touch gestures and standard TV remote D-pad keystrokes into low-latency virtual gamepad inputs routed directly into QEMU virtual machines and arcade emulators.

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rakibdipu/reverse-engineering-hub.git
cd reverse-engineering-hub
```

### 2. Inspect the 50 Projects Catalog
```bash
cat docs/TOP_50_PROJECTS_CATALOG.md
```

### 3. Test Running Key Modules
All 32 Python modules are self-contained and run out-of-the-box:

```bash
# Test the OmniStream TV media engine:
python3 08-merged-omnistream-tv/omnistream_core.py

# Test the Zero-API App & Security Pipeline:
python3 09-merged-app-pipeline/pipeline.py

# Test the SmartTube stream extractor & SponsorBlock query:
python3 12-yuliskov-smarttube/smarttube_stream_extractor.py

# Test the Windows Product Key Validator:
python3 25-witherornot-winkeycheck-licensing/pidgen_validator.py
```

### 4. Running the Creative Craft Apps (Rust + egui)
Each creative desktop app in `02-06` contains a standard `Cargo.toml` and GUI entry point:

```bash
cd 02-photoshop-alternative
cargo run --release
```

---

## 📚 References & Research Papers

| Resource | Source | Topic |
|---|---|---|
| **REA Tool** | [CyberSecurityNews](https://cybersecuritynews.com/reverse-engineer-anything-tool/) | AI Coding Agents + Ghidra / IDA Pro Integration |
| **PS5 Jailbreak Analysis** | [Gizmodo](https://gizmodo.com/the-jailbreak-floodgates-are-opening-for-sonys-playstation-2000823193) | PlayStation 5 Console Firmware & AI Acceleration |
| **Original REA Repository** | [morluto/rea](https://github.com/morluto/rea) | Reverse Engineer Anything MCP Server |
| **CraftApps Suite** | [storytold](https://github.com/storytold) | Open-Source Rust Creative Suite (PhotoCraft, FilmCraft, etc.) |
| **Ghidra Software Reverse Engineering** | [NSA Ghidra](https://ghidra-sre.org/) | NSA Disassembler & Decompiler Framework |

---

## ⚠️ Disclaimer

> This repository and its accompanying source codes are provided strictly for **educational, academic, and security research purposes**. Any analysis of third-party software, firmware, or network protocols should strictly adhere to applicable local laws, authorized penetration testing scopes, and the terms of relevant software licenses.

---

*Authored and curated with care by [MD. RaKib Hassan Dipu](https://github.com/rakibdipu)*
