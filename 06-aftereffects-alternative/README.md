# ✨ Project 06: EffectCraft — Adobe After Effects বিকল্প

> **Rust + WebGPU দিয়ে তৈরি ওপেন-সোর্স Motion Graphics & VFX Compositor**

[![Reference](https://img.shields.io/badge/Inspired%20By-storytold%2Feffectcraft-blue)](https://github.com/storytold/effectcraft)

---

## 📖 কী এটা?

**EffectCraft** হলো Adobe After Effects-এর একটি বিকল্প, যা:
- **Node-based compositing** সাপোর্ট করে
- **Keyframe animation** ও **easing** সমর্থন করে
- Adobe AEP (After Effects Project) ফাইল রিড করে
- GPU-accelerated effects processing

---

## 🔬 After Effects AEP Format — RE Analysis

After Effects-এর `.aep` ফাইল হলো একটি **binary IFF-like format** (RIFX):

```bash
# AEP ফাইল header দেখুন
xxd project.aep | head -20
# 00000000: 5249 4658 xxxx xxxx 4146 5445 ...
#           R I F X         A F T E ...
# এটা RIFX (Big-endian RIFF) ফরম্যাট!
```

### AEP RIFX Structure (Reverse Engineered)

```
RIFX Chunk Structure:
┌─────────────────────────────────────┐
│ FourCC (4 bytes): "RIFX"           │
│ Size (4 bytes, big-endian)          │
│ Form Type (4 bytes): "AFTE"        │
├─────────────────────────────────────┤
│ Nested Chunks:                      │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ "LIST" chunk                    │ │
│ │   Type: "Item" (Project items)  │ │
│ │   Sub-chunks:                   │ │
│ │     "idta" — Item data          │ │
│ │     "Utf8" — Item name (UTF-8)  │ │
│ └─────────────────────────────────┘ │
│                                     │
│ ┌─────────────────────────────────┐ │
│ │ "Layr" chunk (Layer data)       │ │
│ │   "ldta" — Layer timing data    │ │
│ │   "GCst" — Layer group          │ │
│ │   "KFld" — Keyframe data        │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 🦀 Rust Implementation

```rust
// src/formats/aep.rs — After Effects RIFX reader

use std::io::{Read, Seek, SeekFrom};

/// RIFX chunk
#[derive(Debug)]
pub struct RifxChunk {
    pub fourcc: [u8; 4],
    pub size: u32,
    pub data: Vec<u8>,
}

/// AEP Layer (After Effects layer)
#[derive(Debug, Clone)]
pub struct AepLayer {
    pub name: String,
    pub layer_type: LayerType,
    pub in_point: f64,      // seconds
    pub out_point: f64,     // seconds
    pub start_time: f64,
    pub transform: Transform,
    pub keyframes: Vec<Keyframe>,
    pub effects: Vec<Effect>,
    pub blend_mode: BlendMode,
    pub opacity: f32,
    pub visible: bool,
    pub solo: bool,
}

#[derive(Debug, Clone)]
pub enum LayerType {
    Null,
    Solid { color: [f32; 3], width: u32, height: u32 },
    Shape,
    Text,
    Camera,
    Light,
    Footage(String),  // ফাইল পাথ
    Composition(u32), // composition ID
}

/// Transform properties
#[derive(Debug, Clone)]
pub struct Transform {
    pub position: AnimatedVec3,
    pub scale: AnimatedVec3,
    pub rotation: AnimatedF32,
    pub anchor_point: AnimatedVec3,
    pub opacity: AnimatedF32,
}

/// Animated value (keyframes সহ)
#[derive(Debug, Clone)]
pub struct AnimatedF32 {
    pub static_value: f32,
    pub keyframes: Vec<Keyframe>,
}

impl AnimatedF32 {
    /// একটি নির্দিষ্ট সময়ে মান বের করো (interpolate)
    pub fn value_at(&self, time: f64) -> f32 {
        if self.keyframes.is_empty() {
            return self.static_value;
        }

        // সময় অনুযায়ী keyframe খোঁজো
        let before = self.keyframes.iter()
            .filter(|k| k.time <= time)
            .last();
        let after = self.keyframes.iter()
            .find(|k| k.time > time);

        match (before, after) {
            (Some(b), Some(a)) => {
                let t = (time - b.time) / (a.time - b.time);
                let t = apply_easing(t as f32, &b.easing);
                b.value + (a.value - b.value) * t
            }
            (Some(b), None) => b.value,
            (None, Some(a)) => a.value,
            (None, None) => self.static_value,
        }
    }
}

/// Keyframe
#[derive(Debug, Clone)]
pub struct Keyframe {
    pub time: f64,
    pub value: f32,
    pub easing: EasingType,
}

#[derive(Debug, Clone)]
pub enum EasingType {
    Linear,
    EaseIn,
    EaseOut,
    EaseInOut,
    Bezier { x1: f32, y1: f32, x2: f32, y2: f32 },
}

/// Easing function প্রয়োগ করো
pub fn apply_easing(t: f32, easing: &EasingType) -> f32 {
    match easing {
        EasingType::Linear => t,
        EasingType::EaseIn => t * t,
        EasingType::EaseOut => t * (2.0 - t),
        EasingType::EaseInOut => {
            if t < 0.5 { 2.0 * t * t }
            else { -1.0 + (4.0 - 2.0 * t) * t }
        },
        EasingType::Bezier { x1, y1, x2, y2 } => {
            // CSS cubic-bezier approximation
            cubic_bezier_y(t, *x1, *y1, *x2, *y2)
        }
    }
}

fn cubic_bezier_y(t: f32, x1: f32, y1: f32, x2: f32, y2: f32) -> f32 {
    // Newton-Raphson method দিয়ে bezier solve
    let mut guess = t;
    for _ in 0..8 {
        let x = 3.0 * x1 * guess * (1.0-guess) * (1.0-guess)
               + 3.0 * x2 * guess * guess * (1.0-guess)
               + guess * guess * guess;
        let dx = 3.0 * x1 * (1.0-guess) * (1.0-2.0*guess)
                + 3.0 * x2 * guess * (2.0-3.0*guess)
                + 3.0 * guess * guess;
        guess -= (x - t) / dx;
    }
    3.0 * y1 * guess * (1.0-guess) * (1.0-guess)
    + 3.0 * y2 * guess * guess * (1.0-guess)
    + guess * guess * guess
}
```

---

## 🎨 Effect System (GPU Shader-Based)

```wgsl
// shaders/blur.wgsl — Gaussian Blur effect (WGSL WebGPU shader)

@group(0) @binding(0) var input_texture: texture_2d<f32>;
@group(0) @binding(1) var output_texture: texture_storage_2d<rgba8unorm, write>;
@group(0) @binding(2) var<uniform> params: BlurParams;

struct BlurParams {
    radius: f32,
    sigma: f32,
}

/// Gaussian weight বের করো
fn gaussian(x: f32, sigma: f32) -> f32 {
    let TWO_PI: f32 = 6.28318;
    return exp(-0.5 * (x/sigma) * (x/sigma)) / (sigma * sqrt(TWO_PI));
}

@compute @workgroup_size(16, 16)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
    let coord = vec2<i32>(gid.xy);
    let dims = textureDimensions(input_texture);

    if coord.x >= i32(dims.x) || coord.y >= i32(dims.y) {
        return;
    }

    var color = vec4<f32>(0.0);
    var weight_sum: f32 = 0.0;
    let radius = i32(params.radius);

    // Horizontal blur
    for (var x: i32 = -radius; x <= radius; x++) {
        let sample_coord = coord + vec2<i32>(x, 0);
        let clamped = clamp(sample_coord, vec2<i32>(0), vec2<i32>(dims) - 1);
        let w = gaussian(f32(x), params.sigma);
        color += textureLoad(input_texture, clamped, 0) * w;
        weight_sum += w;
    }

    textureStore(output_texture, coord, color / weight_sum);
}
```

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
06-aftereffects-alternative/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── formats/
│   │   └── aep.rs         # After Effects RIFX reader
│   ├── composition/
│   │   ├── layer.rs       # Layer system
│   │   ├── keyframe.rs    # Keyframe animation
│   │   └── render.rs      # Composition renderer
│   ├── effects/
│   │   ├── blur.rs        # Blur effects
│   │   ├── color.rs       # Color correction
│   │   └── distort.rs     # Distortion effects
│   ├── shaders/
│   │   ├── blur.wgsl      # GPU blur shader
│   │   └── composite.wgsl # Compositing shader
│   └── ui/
│       ├── timeline.rs    # Animation timeline
│       └── effects_panel.rs
```

---

## 📚 রিসোর্স

- [wgpu Rust WebGPU](https://wgpu.rs/)
- [Natron (Open Source AE Alternative)](https://github.com/NatronGitHub/Natron)
- [storytold/effectcraft Reference](https://github.com/storytold/effectcraft)
- [After Effects SDK Documentation](https://ae-plugins.docsforadobe.dev/)
