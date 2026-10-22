# 🎨 Project 02: PhotoCraft — Adobe Photoshop বিকল্প

> **Rust-এ লেখা ওপেন-সোর্স Raster Image Editor**

[![Rust](https://img.shields.io/badge/Language-Rust-orange)]()
[![Reference](https://img.shields.io/badge/Inspired%20By-storytold%2Fphotocraft-blue)](https://github.com/storytold/photocraft)

---

## 📖 কী এটা?

**PhotoCraft** হলো Adobe Photoshop-এর একটি ওপেন-সোর্স বিকল্প, যা:
- **Rust** প্রোগ্রামিং ল্যাঙ্গুয়েজে লেখা (মেমোরি-সেফ, দ্রুত)
- **egui** ক্রস-প্ল্যাটফর্ম GUI ফ্রেমওয়ার্ক ব্যবহার করে
- **Photoshop PSD ফাইল** রিড করতে পারে (reverse engineered format)
- Linux, macOS, Windows-এ চলে

---

## 🔬 Photoshop PSD Format — Reverse Engineering

### PSD ফাইল স্ট্রাকচার (RE করে বের করা তথ্য)

```
PSD File Layout:
┌──────────────────────────────────────┐
│ File Header (26 bytes)               │
│   Magic: 0x38425053 ("8BPS")        │
│   Version: 1 (PSD) বা 2 (PSB)       │
│   Channels: 1-56                     │
│   Height: max 30000px (PSD)         │
│   Width: max 30000px (PSD)          │
│   Bit Depth: 1,8,16,32              │
│   Color Mode: RGB=3, CMYK=4 etc.   │
├──────────────────────────────────────┤
│ Color Mode Data                      │
├──────────────────────────────────────┤
│ Image Resources (metadata)           │
│   Resolution, ICC Profile,          │
│   Guides, Slices, etc.              │
├──────────────────────────────────────┤
│ Layer & Mask Information             │
│   Layer records                      │
│   Channel image data                 │
│   Layer blending modes               │
├──────────────────────────────────────┤
│ Image Data (pixel data)              │
│   Compression: Raw/RLE/ZIP          │
└──────────────────────────────────────┘
```

### PSD Parser (Rust Implementation)

```rust
// src/formats/psd.rs — PSD ফাইল রিডার

use std::io::{Read, Seek, SeekFrom};

/// PSD ফাইল হেডার (৩৪ বাইট)
#[derive(Debug, Clone)]
pub struct PsdHeader {
    pub signature: [u8; 4],  // "8BPS"
    pub version: u16,         // 1=PSD, 2=PSB
    pub channels: u16,        // 1-56
    pub height: u32,
    pub width: u32,
    pub bit_depth: u16,       // 1,8,16,32
    pub color_mode: u16,      // 3=RGB, 4=CMYK, 7=Lab
}

/// PSD Layer তথ্য
#[derive(Debug, Clone)]
pub struct PsdLayer {
    pub name: String,
    pub top: i32,
    pub left: i32,
    pub bottom: i32,
    pub right: i32,
    pub opacity: u8,          // 0=transparent, 255=opaque
    pub blending_mode: BlendMode,
    pub visible: bool,
    pub pixels: Vec<u8>,      // RGBA pixel data
}

/// Blending Modes (Photoshop-এর সব mode রিভার্স করা হয়েছে)
#[derive(Debug, Clone, PartialEq)]
pub enum BlendMode {
    Normal,     // "norm"
    Multiply,   // "mul "
    Screen,     // "scrn"
    Overlay,    // "over"
    Darken,     // "dark"
    Lighten,    // "lite"
    HardLight,  // "hLit"
    SoftLight,  // "sLit"
    Difference, // "diff"
    Exclusion,  // "smud"
    // ... আরও
}

impl BlendMode {
    /// PSD 4-byte code থেকে BlendMode তৈরি করো
    pub fn from_bytes(bytes: &[u8; 4]) -> Self {
        match bytes {
            b"norm" => BlendMode::Normal,
            b"mul " => BlendMode::Multiply,
            b"scrn" => BlendMode::Screen,
            b"over" => BlendMode::Overlay,
            b"dark" => BlendMode::Darken,
            b"lite" => BlendMode::Lighten,
            b"hLit" => BlendMode::HardLight,
            b"sLit" => BlendMode::SoftLight,
            b"diff" => BlendMode::Difference,
            b"smud" => BlendMode::Exclusion,
            _ => BlendMode::Normal,
        }
    }
}

/// PSD ফাইল রিডার
pub struct PsdReader<R: Read + Seek> {
    reader: R,
}

impl<R: Read + Seek> PsdReader<R> {
    pub fn new(reader: R) -> Self {
        Self { reader }
    }

    /// PSD হেডার পড়ো
    pub fn read_header(&mut self) -> Result<PsdHeader, PsdError> {
        let mut sig = [0u8; 4];
        self.reader.read_exact(&mut sig)?;

        if &sig != b"8BPS" {
            return Err(PsdError::InvalidMagic);
        }

        let version = self.read_u16()?;
        // 6 bytes reserved
        self.reader.seek(SeekFrom::Current(6))?;

        let channels  = self.read_u16()?;
        let height    = self.read_u32()?;
        let width     = self.read_u32()?;
        let bit_depth = self.read_u16()?;
        let color_mode= self.read_u16()?;

        Ok(PsdHeader {
            signature: sig,
            version,
            channels,
            height,
            width,
            bit_depth,
            color_mode,
        })
    }

    fn read_u16(&mut self) -> Result<u16, PsdError> {
        let mut buf = [0u8; 2];
        self.reader.read_exact(&mut buf)?;
        Ok(u16::from_be_bytes(buf))  // PSD uses big-endian
    }

    fn read_u32(&mut self) -> Result<u32, PsdError> {
        let mut buf = [0u8; 4];
        self.reader.read_exact(&mut buf)?;
        Ok(u32::from_be_bytes(buf))
    }
}

#[derive(Debug)]
pub enum PsdError {
    InvalidMagic,
    Io(std::io::Error),
    UnsupportedVersion(u16),
}

impl From<std::io::Error> for PsdError {
    fn from(e: std::io::Error) -> Self {
        PsdError::Io(e)
    }
}
```

---

## 🎨 Blending Algorithm Implementation

```rust
// src/compositing/blend.rs — Photoshop Blending Modes পুনরায় তৈরি

/// দুটো pixel blend করো (src over dst)
pub fn blend_pixels(src: [f32; 4], dst: [f32; 4], mode: &BlendMode) -> [f32; 4] {
    let [sr, sg, sb, sa] = src;
    let [dr, dg, db, da] = dst;

    let [cr, cg, cb] = match mode {
        BlendMode::Normal   => [sr, sg, sb],
        BlendMode::Multiply => [sr * dr, sg * dg, sb * db],
        BlendMode::Screen   => [
            1.0 - (1.0 - sr) * (1.0 - dr),
            1.0 - (1.0 - sg) * (1.0 - dg),
            1.0 - (1.0 - sb) * (1.0 - db),
        ],
        BlendMode::Overlay  => [
            overlay_channel(sr, dr),
            overlay_channel(sg, dg),
            overlay_channel(sb, db),
        ],
        BlendMode::Difference => [
            (sr - dr).abs(),
            (sg - dg).abs(),
            (sb - db).abs(),
        ],
        _ => [sr, sg, sb],
    };

    // Alpha compositing (Porter-Duff "over" operation)
    let out_a = sa + da * (1.0 - sa);
    let out_r = (cr * sa + dr * da * (1.0 - sa)) / out_a;
    let out_g = (cg * sa + dg * da * (1.0 - sa)) / out_a;
    let out_b = (cb * sa + db * da * (1.0 - sa)) / out_a;

    [out_r, out_g, out_b, out_a]
}

fn overlay_channel(a: f32, b: f32) -> f32 {
    if b < 0.5 {
        2.0 * a * b
    } else {
        1.0 - 2.0 * (1.0 - a) * (1.0 - b)
    }
}
```

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
02-photoshop-alternative/
├── Cargo.toml
├── src/
│   ├── main.rs              # Entry point, egui app
│   ├── app.rs               # Main application state
│   ├── canvas/
│   │   ├── mod.rs           # Canvas rendering
│   │   ├── layers.rs        # Layer management
│   │   └── selection.rs     # Selection tools
│   ├── tools/
│   │   ├── brush.rs         # Brush tool
│   │   ├── eraser.rs        # Eraser tool
│   │   ├── clone_stamp.rs   # Clone Stamp
│   │   └── healing.rs       # Healing Brush
│   ├── formats/
│   │   ├── psd.rs           # PSD reader/writer
│   │   ├── png.rs           # PNG support
│   │   └── jpg.rs           # JPEG support
│   ├── compositing/
│   │   ├── blend.rs         # Blending modes
│   │   └── filters.rs       # Image filters
│   └── ui/
│       ├── toolbar.rs       # Tool palette
│       ├── layers_panel.rs  # Layers panel
│       └── properties.rs    # Properties panel
└── assets/
    ├── icons/               # UI icons
    └── brushes/             # Default brush presets
```

---

## 🚀 বিল্ড ও রান

```bash
# Dependencies ইনস্টল করুন (Rust)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# প্রজেক্ট বিল্ড করুন
cd 02-photoshop-alternative
cargo build --release

# চালান
./target/release/photocraft
```

---

## 🔬 RE পদ্ধতি: Photoshop কীভাবে রিভার্স করা হয়েছে

1. **Wireshark** দিয়ে Photoshop-এর নেটওয়ার্ক কল দেখা
2. **Ghidra** দিয়ে Photoshop.exe-এর PSD parser ফাংশন বের করা
3. **REA Tool** ব্যবহার করে AI-assisted code analysis
4. **Fuzzing** দিয়ে edge cases বের করা
5. **Adobe PSD Specification** (publicly available) রেফারেন্স হিসেবে ব্যবহার

---

## 📚 রিসোর্স

- [Adobe PSD Spec (Public)](https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/)
- [libpsd (C library)](https://github.com/libpsd/libpsd)
- [psd.py (Python)](https://github.com/kmike/psd-tools)
- [storytold/photocraft Reference](https://github.com/storytold/photocraft)
