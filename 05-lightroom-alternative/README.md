# 📷 Project 05: LightCraft — Adobe Lightroom বিকল্প

> **Rust-এ লেখা ওপেন-সোর্স RAW Photo Processor**

[![Reference](https://img.shields.io/badge/Inspired%20By-storytold%2Flightcraft-blue)](https://github.com/storytold/lightcraft)

---

## 📖 কী এটা?

**LightCraft** হলো Adobe Lightroom-এর একটি বিকল্প, বিশেষত:
- **RAW ফাইল** প্রসেসিং (Canon CR2, Nikon NEF, Sony ARW ইত্যাদি)
- **Lightroom Catalog (.lrcat)** ফরম্যাট রিড করে
- Non-destructive photo editing
- AI-powered photo enhancement

---

## 🔬 Lightroom Catalog Format — RE Analysis

Lightroom-এর `.lrcat` ফাইল আসলে একটি **SQLite database**!

```bash
# LRCAT ফাইল কী সেটা দেখুন
file Lightroom\ Catalog.lrcat
# Output: Lightroom Catalog.lrcat: SQLite 3.x database

# SQLite দিয়ে খুলুন
sqlite3 "Lightroom Catalog.lrcat"

# Tables দেখুন
.tables
```

### LRCAT Database Schema (RE করা)

```sql
-- প্রধান tables যা Ghidra + SQLite browser দিয়ে বের করা হয়েছে

-- ছবির মেটাডেটা
CREATE TABLE Adobe_images (
    id_local    INTEGER PRIMARY KEY,
    id_global   VARCHAR(36),     -- UUID
    rootFile    INTEGER,         -- file reference
    captureTime VARCHAR(25),     -- "2024-01-15T10:30:00"
    rating      INTEGER,         -- 0-5 stars
    colorLabels VARCHAR(10),     -- "red", "green" etc.
    pick        INTEGER          -- flagged: 1, rejected: -1
);

-- এডিট সেটিংস (Non-destructive adjustments)
CREATE TABLE Adobe_libraryImageDevelopSettings (
    image           INTEGER REFERENCES Adobe_images(id_local),
    developPreset   TEXT,        -- JSON encoded settings!
    -- সেটিংস JSON ফরম্যাটে থাকে
    hasDevelopAdjustments INTEGER
);

-- Keywords/Tags
CREATE TABLE AgLibraryKeyword (
    id_local    INTEGER PRIMARY KEY,
    lc_name     VARCHAR,         -- keyword নাম (lowercase)
    name        VARCHAR          -- keyword নাম
);

-- Collection (Albums)
CREATE TABLE AgLibraryCollection (
    id_local    INTEGER PRIMARY KEY,
    name        VARCHAR,
    creationId  VARCHAR(36)
);

-- ফাইলের physical পাথ
CREATE TABLE AgLibraryRootFolder (
    id_local    INTEGER PRIMARY KEY,
    absolutePath VARCHAR           -- ফোল্ডারের path
);
```

### Develop Settings JSON (RE করা)

```json
{
  "Exposure": 0.5,
  "Contrast": 10,
  "Highlights": -30,
  "Shadows": 20,
  "Whites": 5,
  "Blacks": -10,
  "Clarity": 15,
  "Vibrance": 20,
  "Saturation": 5,
  "Temperature": 5500,
  "Tint": -5,
  "ToneCurve": {
    "ParametricHighlights": 25,
    "ParametricLights": 10,
    "ParametricDarks": -10,
    "ParametricShadows": -25
  },
  "HueAdjustmentRed": 0,
  "SaturationAdjustmentRed": 20,
  "LuminanceAdjustmentRed": 10,
  "GrainAmount": 20,
  "GrainSize": 25,
  "VignetteAmount": -20
}
```

---

## 🦀 Rust Implementation

```rust
// src/catalog/lrcat.rs — Lightroom Catalog Reader

use rusqlite::{Connection, Result};

/// Lightroom ছবির তথ্য
#[derive(Debug, Clone)]
pub struct LightroomImage {
    pub id: i64,
    pub uuid: String,
    pub capture_time: Option<String>,
    pub rating: i32,
    pub pick: i32,
    pub file_path: Option<String>,
    pub develop_settings: Option<DevelopSettings>,
}

/// Photo adjustment settings
#[derive(Debug, Clone, serde::Deserialize)]
pub struct DevelopSettings {
    #[serde(rename = "Exposure")]
    pub exposure: f32,           // -5.0 to +5.0

    #[serde(rename = "Contrast")]
    pub contrast: f32,           // -100 to +100

    #[serde(rename = "Highlights")]
    pub highlights: f32,

    #[serde(rename = "Shadows")]
    pub shadows: f32,

    #[serde(rename = "Temperature")]
    pub temperature: Option<i32>, // 2000K - 50000K (Kelvin)

    #[serde(rename = "Tint")]
    pub tint: Option<i32>,       // -150 to +150

    #[serde(rename = "Saturation")]
    pub saturation: Option<f32>,

    #[serde(rename = "Clarity")]
    pub clarity: Option<f32>,
}

impl Default for DevelopSettings {
    fn default() -> Self {
        Self {
            exposure: 0.0,
            contrast: 0.0,
            highlights: 0.0,
            shadows: 0.0,
            temperature: Some(5500),
            tint: Some(0),
            saturation: Some(0.0),
            clarity: Some(0.0),
        }
    }
}

/// Lightroom Catalog reader
pub struct LrcatReader {
    conn: Connection,
}

impl LrcatReader {
    /// LRCAT ফাইল খুলো
    pub fn open(path: &str) -> Result<Self> {
        let conn = Connection::open(path)?;
        Ok(Self { conn })
    }

    /// সব ছবির তালিকা আনো
    pub fn get_all_images(&self) -> Result<Vec<LightroomImage>> {
        let mut stmt = self.conn.prepare(
            "SELECT i.id_local, i.id_global, i.captureTime, i.rating, i.pick
             FROM Adobe_images i
             ORDER BY i.captureTime DESC
             LIMIT 1000"
        )?;

        let images = stmt.query_map([], |row| {
            Ok(LightroomImage {
                id: row.get(0)?,
                uuid: row.get(1).unwrap_or_default(),
                capture_time: row.get(2)?,
                rating: row.get(3).unwrap_or(0),
                pick: row.get(4).unwrap_or(0),
                file_path: None,
                develop_settings: None,
            })
        })?
        .filter_map(|r| r.ok())
        .collect();

        Ok(images)
    }

    /// একটি ছবির develop settings আনো
    pub fn get_develop_settings(&self, image_id: i64) -> Option<DevelopSettings> {
        let result: rusqlite::Result<String> = self.conn.query_row(
            "SELECT developPreset FROM Adobe_libraryImageDevelopSettings WHERE image = ?1",
            [image_id],
            |row| row.get(0),
        );

        result.ok()
            .and_then(|json| serde_json::from_str(&json).ok())
    }

    /// ছবি export করো (settings apply করে)
    pub fn export_image(&self, image: &LightroomImage, output_path: &str) -> Result<(), String> {
        let settings = image.develop_settings.clone().unwrap_or_default();
        // TODO: RAW processing + settings apply
        Ok(())
    }
}
```

### RAW Image Processing Pipeline

```rust
// src/raw/processor.rs — RAW ফাইল প্রসেসিং

/// RAW processing steps (Lightroom যেভাবে করে RE করা হয়েছে)
pub struct RawProcessor {
    settings: DevelopSettings,
}

impl RawProcessor {
    /// RAW → RGBA pixel array তৈরি করো
    pub fn process(&self, raw_data: &[u8]) -> Vec<u8> {
        // ধাপ ১: Demosaic (Bayer pattern → RGB)
        let mut pixels = self.demosaic(raw_data);

        // ধাপ ২: White Balance (Temperature + Tint)
        self.apply_white_balance(&mut pixels);

        // ধাপ ৩: Exposure
        self.apply_exposure(&mut pixels);

        // ধাপ ৪: Tone Curve
        self.apply_tone_curve(&mut pixels);

        // ধাপ ৫: HSL (Hue, Saturation, Luminance)
        self.apply_hsl(&mut pixels);

        // ধাপ ৬: Sharpening + Noise Reduction
        self.apply_sharpening(&mut pixels);

        pixels
    }

    fn apply_exposure(&self, pixels: &mut Vec<u8>) {
        let factor = 2f32.powf(self.settings.exposure);
        for pixel in pixels.chunks_mut(4) {
            pixel[0] = ((pixel[0] as f32 * factor).min(255.0)) as u8;
            pixel[1] = ((pixel[1] as f32 * factor).min(255.0)) as u8;
            pixel[2] = ((pixel[2] as f32 * factor).min(255.0)) as u8;
        }
    }

    fn apply_white_balance(&self, pixels: &mut Vec<u8>) {
        let temp = self.settings.temperature.unwrap_or(5500) as f32;
        let tint = self.settings.tint.unwrap_or(0) as f32;

        // Kelvin থেকে RGB multiplier বের করো
        let (r_mult, g_mult, b_mult) = kelvin_to_rgb_multiplier(temp, tint);

        for pixel in pixels.chunks_mut(4) {
            pixel[0] = ((pixel[0] as f32 * r_mult).min(255.0)) as u8;
            pixel[1] = ((pixel[1] as f32 * g_mult).min(255.0)) as u8;
            pixel[2] = ((pixel[2] as f32 * b_mult).min(255.0)) as u8;
        }
    }

    fn demosaic(&self, _raw: &[u8]) -> Vec<u8> {
        // Simplified — real implementation uses libraw
        vec![]
    }

    fn apply_tone_curve(&self, _pixels: &mut Vec<u8>) {}
    fn apply_hsl(&self, _pixels: &mut Vec<u8>) {}
    fn apply_sharpening(&self, _pixels: &mut Vec<u8>) {}
}

fn kelvin_to_rgb_multiplier(temp: f32, tint: f32) -> (f32, f32, f32) {
    // সরলীকৃত Color Temperature অ্যালগরিদম
    let r = if temp <= 6600.0 { 1.0 } else { (temp / 6600.0 - 1.0).powf(-0.1332) * 1.292 };
    let b = if temp >= 6600.0 { 1.0 } else { ((temp - 1900.0) / 900.0).ln() * 0.543 };
    let g = 1.0 + tint / 1000.0;
    (r.min(1.0), g.min(1.0), b.min(1.0))
}
```

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
05-lightroom-alternative/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── catalog/
│   │   └── lrcat.rs       # Lightroom catalog reader
│   ├── raw/
│   │   ├── processor.rs   # RAW processing
│   │   └── libraw.rs      # libraw FFI bindings
│   ├── adjustments/
│   │   ├── exposure.rs
│   │   ├── color.rs
│   │   └── tone_curve.rs
│   └── ui/
│       ├── library.rs     # Photo library view
│       └── develop.rs     # Develop/Edit panel
```

---

## 📚 রিসোর্স

- [libraw (C++ RAW library)](https://github.com/LibRaw/LibRaw)
- [darktable Source (Reference NLE)](https://github.com/darktable-org/darktable)
- [storytold/lightcraft Reference](https://github.com/storytold/lightcraft)
- [Adobe DNG Specification](https://helpx.adobe.com/photoshop/using/adobe-dng-converter.html)
