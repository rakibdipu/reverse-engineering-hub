# ✏️ Project 03: VectorCraft — Open-Source Illustrator Alternative

> **Pure Rust + egui Vector Graphics Editor with Bezier Math & SVG/AI File Support**

[![Rust](https://img.shields.io/badge/Language-Rust-orange.svg)]()
[![Inspiration](https://img.shields.io/badge/Inspired%20By-storytold%2Fvectorcraft-blue.svg)](https://github.com/storytold/vectorcraft)

---

## 👤 Upstream Creator & Attribution
* **Original Author / Inspiration:** [@storytold](https://github.com/storytold/vectorcraft)
* **Upstream Repository:** [https://github.com/storytold/vectorcraft](https://github.com/storytold/vectorcraft)
* **Credit & License:** All original architectural concepts belong to @storytold. This repository provides an upgraded, documented, and runnable standalone implementation.

---

## 🚀 How We Made It Better / Merged Innovations
- Includes complete runnable `egui` desktop UI entrypoint with vector pen tools, stroke/fill controls, and canvas.
- De Casteljau cubic Bezier curve engine with subdivision flattening and tangent calculation.
- SVG path data parser (M, L, C, Z commands) and PostScript Adobe Illustrator format analysis.
- Complete `Cargo.toml` with release optimization profiles.

---

## 🔬 Adobe Illustrator AI & SVG Format Analysis

Adobe Illustrator (`.ai`) files historically wrap PostScript within a PDF container. VectorCraft reverse engineers these vector commands to construct native paths.

### Cubic Bezier Curve Math (De Casteljau's Algorithm)

```rust
#[derive(Debug, Clone, Copy)]
pub struct CubicBezier {
    pub p0: Vec2,  // Start point
    pub p1: Vec2,  // Control point 1
    pub p2: Vec2,  // Control point 2
    pub p3: Vec2,  // End point
}

impl CubicBezier {
    pub fn point_at(&self, t: f32) -> Vec2 {
        let u = 1.0 - t;
        self.p0 * (u * u * u)
          + self.p1 * (3.0 * u * u * t)
          + self.p2 * (3.0 * u * t * t)
          + self.p3 * (t * t * t)
    }

    pub fn tangent_at(&self, t: f32) -> Vec2 {
        let u = 1.0 - t;
        (self.p1 - self.p0) * (3.0 * u * u)
          + (self.p2 - self.p1) * (6.0 * u * t)
          + (self.p3 - self.p2) * (3.0 * t * t)
    }

    pub fn split(&self, t: f32) -> (CubicBezier, CubicBezier) {
        let q0 = self.p0.lerp(self.p1, t);
        let q1 = self.p1.lerp(self.p2, t);
        let q2 = self.p2.lerp(self.p3, t);
        let r0 = q0.lerp(q1, t);
        let r1 = q1.lerp(q2, t);
        let s = r0.lerp(r1, t);

        (
            CubicBezier { p0: self.p0, p1: q0, p2: r0, p3: s },
            CubicBezier { p0: s, p1: r1, p2: q2, p3: self.p3 },
        )
    }
}
```

---

## 🚀 Building & Running

```bash
cargo build --release
cargo run --release
```