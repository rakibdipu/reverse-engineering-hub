# ⚡ Zero-API Headless App & Media Pipeline

> **Unified Innovation Merging Multiple Groundbreaking Upstream Repositories**

---

## 👤 Original Creators & Upstream Attribution
This mega-project stands on the shoulders of giants. We express our deepest respect and gratitude to the primary creators:
* @WitherOrNot (gplayapi, uupget, mpclient)\n* @yuliskov (PoTokenService)

All foundational reverse engineering, API extraction, and protocols originated from their respective upstream repositories.

---

## 🚀 Why This Merged Version Is Better
- **Zero Subscription Fees**: Completely avoids paid APIs by directly communicating with original endpoints (Play Store, Microsoft UUP, YouTube InnerTube).\n- **Instant Security Audit**: Every downloaded APK or Windows package is scanned on-the-fly using the native Microsoft Defender engine (mpengine.dll).\n- **Automated Bot Bypass**: Embedded PoToken generator prevents YouTube 403 Forbidden errors during automated media extraction.\n- **End-to-End Headless**: Can be deployed on headless Linux or Windows servers as an automated asset pipeline.

---
# ⚡ Project 09: Zero-API App & Media Pipeline

> **Merged Project: gplayapi + uupget + mpclient + PoTokenService**

## 📖 প্রজেক্ট ওভারভিউ
কোনো অফিশিয়াল পেইড API সাবস্ক্রিপশন ছাড়াই হেডলেসভাবে অ্যান্ড্রয়েড অ্যাপ (.apk), উইন্ডোজ অফিশিয়াল আপডেট (.esd/.cab) এবং ইউটিউব মিডিয়া স্ট্রিম সংগ্রহ করে সরাসরি উইন্ডোজ ডিফেন্ডার দিয়ে ভাইরাস স্ক্যান করার পাইপলাইন।

### 🧩 কোন প্রজেক্টগুলো মার্জ করা হয়েছে:
1. **WitherOrNot/gplayapi**: গুগল প্লে স্টোর থেকে সরাসরি অরিজিনাল APK ডাউনলোড।
2. **WitherOrNot/uupget**: মাইক্রোসফটের UUP সার্ভার থেকে সরাসরি উইন্ডোজ আপডেট ডাউনলোড।
3. **WitherOrNot/mpclient**: উইন্ডোজ ডিফেন্ডারের ইঞ্জিন (`mpengine.dll`) দিয়ে তাৎক্ষণিক ভাইরাস স্ক্যান।
4. **yuliskov/PoTokenService**: থ্রটলিং ছাড়া হাই-স্পিড ভিডিও স্ট্রিম ক্যাশিং।

## 🏗️ ওয়ার্কফ্লো
```
[User Request] 
      │
      ├───► [gplayapi] ────► Download APK ────► [mpclient scan] ──► Verified Safe
      ├───► [uupget]   ────► Download Windows CAB ──► [CBS Verify] ──► Ready
      └───► [PoToken]  ────► YouTube Stream ──► High-speed Cache ──► Output
```
