# 🎬 Project 04: FilmCraft — Open-Source Premiere Pro Alternative

> **Non-Linear Video Editor (NLE) with Adobe Premiere PRPROJ Parser & WebGPU Timeline Rendering**

[![Rust](https://img.shields.io/badge/Language-Rust-orange.svg)]()
[![Inspiration](https://img.shields.io/badge/Inspired%20By-storytold%2Ffilmcraft-blue.svg)](https://github.com/storytold/filmcraft)

---

## 👤 Upstream Creator & Attribution
* **Original Author / Inspiration:** [@storytold](https://github.com/storytold/filmcraft)
* **Upstream Repository:** [https://github.com/storytold/filmcraft](https://github.com/storytold/filmcraft)
* **Credit & License:** All original architectural concepts belong to @storytold. This repository provides an upgraded, documented, and runnable standalone implementation.

---

## 🚀 How We Made It Better / Merged Innovations
- Includes complete runnable `egui` desktop UI entrypoint with timeline tracks (V1, V2, A1, A2), media bin, and preview monitor.
- Reverse-engineered Adobe Premiere PRPROJ XML structure parser with automatic gzip decompression.
- Non-linear timeline playback engine with frame-accurate playhead tracking.
- Complete `Cargo.toml` with release optimization profiles.

---

## 🔬 Adobe Premiere PRPROJ Format Analysis

Adobe Premiere Pro (`.prproj`) project files are gzip-compressed XML documents.

```bash
# Decompress and inspect PRPROJ XML:
gzip -dc project.prproj | head -n 30
```

### PRPROJ XML Parser (Rust)

```rust
use serde::Deserialize;
use flate2::read::GzDecoder;
use std::io::Read;

#[derive(Debug, Deserialize)]
#[serde(rename = "PremiereData")]
pub struct PremiereProject {
    #[serde(rename = "Version")]
    pub version: String,
    #[serde(rename = "Sequence", default)]
    pub sequences: Vec<Sequence>,
}

#[derive(Debug, Deserialize)]
pub struct Sequence {
    #[serde(rename = "Name")]
    pub name: String,
}

pub fn load_prproj(path: &str) -> Result<PremiereProject, Box<dyn std::error::Error>> {
    let file = std::fs::File::open(path)?;
    let mut decoder = GzDecoder::new(file);
    let mut xml = String::new();
    decoder.read_to_string(&mut xml)?;
    let project: PremiereProject = quick_xml::de::from_str(&xml)?;
    Ok(project)
}
```

---

## 🚀 Building & Running

```bash
cargo build --release
cargo run --release
```