# ⚡ Project 09: Zero-API Headless App & Media Pipeline

> **Automated Package Extraction & Antivirus Audit Merging gplayapi, uupget, mpclient & PoTokenService**

---

## 👤 Original Creators & Upstream Attribution
This mega-project stands on the shoulders of giants. We express our deepest respect and gratitude to the primary creators:
* **[@WitherOrNot](https://github.com/WitherOrNot)** (gplayapi, uupget, mpclient)
* **[@yuliskov](https://github.com/yuliskov)** (PoTokenService)

All foundational reverse engineering, API extraction, and protocols originated from their respective upstream repositories.

---

## 🚀 Why This Merged Version Is Better
- **Zero Subscription Fees:** Completely avoids costly third-party API keys by communicating directly with official endpoints (Google Play Store, Microsoft UUP catalog, YouTube InnerTube).
- **Automated Security Verification:** Every retrieved APK or Windows update CAB/ESD is immediately scanned via the native Microsoft Defender scanning engine (`mpengine.dll`).
- **Bot-Detection Immunity:** Embedded PoToken management prevents YouTube 403 Forbidden errors during high-throughput media extraction.
- **Headless Automation:** Runs as a unified CLI or daemon pipeline on headless Linux/Windows environments.

---

## 🏗️ Workflow

```
[Target Request] 
      │
      ├───► [gplayapi] ────► Download APK ────► [mpclient scan] ──► Verified Safe
      ├───► [uupget]   ────► Download Windows CAB ──► [CBS Verify] ──► Verified Safe
      └───► [PoToken]  ────► YouTube Stream ──► High-speed Cache ──► Ready
```

---

## 🚀 Quick Start

```bash
# Execute the automated pipeline:
python3 pipeline.py
```
