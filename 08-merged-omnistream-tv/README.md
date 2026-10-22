# 📺 Project 08: OmniStream TV

> **Merged Project: SmartTube + MediaServiceCore + LeanKeyboard + PlexTraktSync + Sonarr/Radarr**

## 📖 প্রজেক্ট ওভারভিউ
OmniStream TV হলো একটি অল-ইন-ওয়ান ওপেন-সোর্স স্মার্ট টিভি ও হোম থিয়েটার মিডিয়া সেন্টার। এটি ইউটিউব ও লোকাল মিডিয়া সার্ভারকে একসাথে যুক্ত করে একটি নিরবচ্ছিন্ন রিমোট-ফ্রেন্ডলি ইন্টারফেস প্রদান করে।

### 🧩 কোন প্রজেক্টগুলো মার্জ করা হয়েছে:
1. **yuliskov/SmartTube**: 4K HDR প্লেয়ার ইঞ্জিন, স্পন্সরব্লক ও নো-অ্যাড আর্কিটেকচার।
2. **yuliskov/MediaServiceCore**: আনঅফিসিয়াল InnerTube API এক্সট্র্যাক্টর।
3. **yuliskov/LeanKeyboard**: রিমোটের D-pad দিয়ে দ্রুত টাইপিংয়ের জন্য কাস্টম অন-স্ক্রিন কিবোর্ড।
4. **stevietv/PlexTraktSync**: রিয়েল-টাইম ওয়াচ হিস্ট্রি ও ট্র্যাকিং Trakt.tv-এর সাথে সিঙ্ক।
5. **stevietv/Sonarr & Radarr**: সরাসরি টিভি থেকে নতুন মুভি/সিরিজ রিকোয়েস্ট অটোমেশন।

## 🏗️ আর্কিটেকচার
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

## 🚀 দ্রুত শুরু করুন
```bash
# OmniStream TV ডেমো লঞ্চার
python3 omnistream_core.py
```
