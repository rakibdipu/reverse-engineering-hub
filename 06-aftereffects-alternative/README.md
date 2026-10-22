# ✨ Project 06: EffectCraft — Open-Source After Effects Alternative

> **Node-Based Motion Graphics & VFX Compositor with AEP RIFX Binary Chunk Parser & WGSL Shaders**

[![Rust](https://img.shields.io/badge/Language-Rust-orange.svg)]()
[![Inspiration](https://img.shields.io/badge/Inspired%20By-storytold%2Feffectcraft-blue.svg)](https://github.com/storytold/effectcraft)

---

## 👤 Upstream Creator & Attribution
* **Original Author / Inspiration:** [@storytold](https://github.com/storytold/effectcraft)
* **Upstream Repository:** [https://github.com/storytold/effectcraft](https://github.com/storytold/effectcraft)
* **Credit & License:** All original architectural concepts belong to @storytold. This repository provides an upgraded, documented, and runnable standalone implementation.

---

## 🚀 How We Made It Better / Merged Innovations
- Includes complete runnable `egui` desktop UI entrypoint with composition layer stack, timeline keyframes, and preview monitor.
- Reverse-engineered Adobe After Effects AEP (RIFX binary chunk) reader.
- Keyframe easing engine with Newton-Raphson cubic-bezier solver and WGSL Gaussian blur compute shader.
- Complete `Cargo.toml` with release optimization profiles.

---

## 🔬 After Effects AEP Format Analysis

After Effects project files (`.aep`) use the big-endian RIFF (`RIFX`) binary chunk container with Form Type `AFTE`.

```
RIFX Chunk Structure:
┌─────────────────────────────────────┐
│ FourCC (4 bytes): "RIFX"           │
│ Size (4 bytes, big-endian)          │
│ Form Type (4 bytes): "AFTE"        │
├─────────────────────────────────────┤
│ Nested Chunks:                      │
│   LIST -> Item (Project media items)│
│   Layr -> Layer timing & transforms │
│   KFld -> Keyframe animation data   │
└─────────────────────────────────────┘
```

---

## 🚀 Building & Running

```bash
cargo build --release
cargo run --release
```