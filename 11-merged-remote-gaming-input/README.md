# 🎮 Project 11: Virtual Remote Gaming & Emulation Controller

> **Cross-Device Virtual Controller Merging chunithm-vcontroller, LeanKeyboard & qemui**

---

## 👤 Original Creators & Upstream Attribution
This mega-project stands on the shoulders of giants. We express our deepest respect and gratitude to the primary creators:
* **[@WitherOrNot](https://github.com/WitherOrNot)** (chunithm-vcontroller, qemui)
* **[@yuliskov](https://github.com/yuliskov)** (LeanKeyboard)

All foundational reverse engineering, API extraction, and protocols originated from their respective upstream repositories.

---

## 🚀 Why This Merged Version Is Better
- **Cross-Device Input Translation:** Converts mobile touch sensors and Android TV remote D-pad presses into virtual gamepad buttons and analog sticks.
- **Direct Emulation Passthrough:** Maps keycodes and touch coordinates directly into QEMU virtual machines and arcade emulators without third-party joypad daemons.
- **Low-Latency Architecture:** Asynchronous socket-level event transmission guarantees minimal input latency for fast-paced rhythm and arcade gaming.

---

## 🚀 Quick Start

```bash
# Test virtual gamepad key mapping:
python3 virtual_controller.py
```
