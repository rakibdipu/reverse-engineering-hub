# SmartTube & SmartTubeLegacy

> **Enhanced Open-Source Implementation based on upstream research**

---

## 👤 Upstream Creator & Attribution
* **Original Creator:** **[@yuliskov (Yuriy L)](https://github.com/yuliskov/SmartTube)**
* **Upstream Repository:** [https://github.com/yuliskov/SmartTube](https://github.com/yuliskov/SmartTube)
* **License & Credit:** All original architecture and engineering concepts belong to @yuliskov (Yuriy L). This repository provides an upgraded, standalone, and cross-platform implementation.

---

## 🚀 How We Made It Better / What Was Merged
- Extracted core streaming logic into standalone, cross-platform Python module without requiring full Android SDK to inspect.\n- Direct integration with modern AV1/Opus stream format selection and live SponsorBlock REST endpoints.\n- Decoupled from Android Leanback UI so the stream extraction engine can be run on headless servers, NAS, or desktop players.

---

## 🛠️ Included Working Implementation
Run the included module directly from this directory:

```bash
python3 smarttube_stream_extractor.py
```
