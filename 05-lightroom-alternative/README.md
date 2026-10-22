# 📷 Project 05: LightCraft — Open-Source Lightroom Alternative

> **Non-Destructive RAW Photo Processor with Adobe Lightroom Catalog (.lrcat) SQLite Parser**

[![Rust](https://img.shields.io/badge/Language-Rust-orange.svg)]()
[![Inspiration](https://img.shields.io/badge/Inspired%20By-storytold%2Flightcraft-blue.svg)](https://github.com/storytold/lightcraft)

---

## 👤 Upstream Creator & Attribution
* **Original Author / Inspiration:** [@storytold](https://github.com/storytold/lightcraft)
* **Upstream Repository:** [https://github.com/storytold/lightcraft](https://github.com/storytold/lightcraft)
* **Credit & License:** All original architectural concepts belong to @storytold. This repository provides an upgraded, documented, and runnable standalone implementation.

---

## 🚀 How We Made It Better / Merged Innovations
- Includes complete runnable `egui` desktop UI entrypoint with Develop adjustments panel (Exposure, Temp, Highlights, Shadows).
- Reverse-engineered Adobe Lightroom Catalog (`.lrcat`) SQLite database schema reader.
- Color temperature algorithm converting Kelvin and Tint values into RGB multipliers.
- Complete `Cargo.toml` with release optimization profiles.

---

## 🔬 Lightroom Catalog (.lrcat) Reverse Engineering

Adobe Lightroom catalogs (`.lrcat`) are SQLite 3 databases storing image metadata and non-destructive JSON adjustment presets.

```sql
-- Core Lightroom Catalog Schema:
CREATE TABLE Adobe_images (
    id_local    INTEGER PRIMARY KEY,
    id_global   VARCHAR(36),
    captureTime VARCHAR(25),
    rating      INTEGER,
    pick        INTEGER
);

CREATE TABLE Adobe_libraryImageDevelopSettings (
    image           INTEGER REFERENCES Adobe_images(id_local),
    developPreset   TEXT,  -- JSON-encoded adjustments!
    hasDevelopAdjustments INTEGER
);
```

### Color Temperature to RGB Conversion Algorithm

```rust
pub fn kelvin_to_rgb_multiplier(temp_kelvin: f32, tint: f32) -> (f32, f32, f32) {
    let r = if temp_kelvin <= 6600.0 {
        1.0
    } else {
        (temp_kelvin / 6600.0 - 1.0).powf(-0.1332) * 1.292
    };

    let b = if temp_kelvin >= 6600.0 {
        1.0
    } else {
        ((temp_kelvin - 1900.0) / 900.0).ln() * 0.543
    };

    let g = 1.0 + (tint / 1000.0);
    (r.clamp(0.0, 1.0), g.clamp(0.0, 1.0), b.clamp(0.0, 1.0))
}
```

---

## 🚀 Building & Running

```bash
cargo build --release
cargo run --release
```