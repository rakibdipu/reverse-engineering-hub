# ✏️ Project 03: VectorCraft — Adobe Illustrator বিকল্প

> **Rust-এ লেখা ওপেন-সোর্স Vector Graphics Editor**

[![Rust](https://img.shields.io/badge/Language-Rust-orange)]()
[![Reference](https://img.shields.io/badge/Inspired%20By-storytold%2Fvectorcraft-blue)](https://github.com/storytold/vectorcraft)

---

## 📖 কী এটা?

**VectorCraft** হলো Adobe Illustrator-এর একটি ওপেন-সোর্স বিকল্প, যা:
- **SVG**, **AI**, **EPS** ফাইল ফরম্যাট সাপোর্ট করে
- বেজিয়ার কার্ভ, পথ সম্পাদনা, ভেক্টর আঁকা
- **Adobe AI ফরম্যাট** রিভার্স ইঞ্জিনিয়ারিং করে পড়তে পারে

---

## 🔬 Adobe AI Format — Reverse Engineering

Adobe Illustrator (.ai) ফাইল মূলত **PostScript** ভিত্তিক এবং একটি **PDF wrapper** ব্যবহার করে।

### AI File Structure (RE Analysis)

```
Adobe Illustrator File:
┌─────────────────────────────────────┐
│ PDF Header (%PDF-1.x)              │
│ AI Header (%!PS-Adobe-3.0)         │
├─────────────────────────────────────┤
│ AI Preamble                         │
│   Creator, Creation Date            │
│   Document Setup                    │
├─────────────────────────────────────┤
│ AI Document Data (PostScript)       │
│   %%BeginDocument                   │
│   Vector paths (Bezier curves)      │
│   Colors (CMYK/RGB/Spot)           │
│   Text objects                      │
│   Gradients                         │
│   %%EndDocument                     │
├─────────────────────────────────────┤
│ PDF XRef Table                      │
│ PDF Trailer                         │
└─────────────────────────────────────┘
```

### PostScript Path Commands (AI-তে যেভাবে ব্যবহার হয়)

```postscript
% AI Path Example (Reverse Engineered)
% moveto, lineto, curveto = Bezier curves

100 200 moveto          % শুরু বিন্দু
300 200 lineto          % সরলরেখা
400 400 curveto         % বেজিয়ার কার্ভ (simplified)
100 200 lineto          % ফিরে আসা
closepath               % পথ বন্ধ
stroke                  % রেখা আঁকো
```

---

## 🦀 Rust Implementation

```rust
// src/geometry/bezier.rs — Bezier Curve Engine

/// কিউবিক বেজিয়ার কার্ভ
#[derive(Debug, Clone, Copy)]
pub struct CubicBezier {
    pub p0: Vec2,  // শুরু বিন্দু
    pub p1: Vec2,  // Control point 1
    pub p2: Vec2,  // Control point 2
    pub p3: Vec2,  // শেষ বিন্দু
}

impl CubicBezier {
    /// t (0.0 থেকে 1.0) সময়ে কার্ভের বিন্দু বের করো
    pub fn point_at(&self, t: f32) -> Vec2 {
        let u = 1.0 - t;
        // De Casteljau's algorithm
        self.p0 * (u * u * u)
          + self.p1 * (3.0 * u * u * t)
          + self.p2 * (3.0 * u * t * t)
          + self.p3 * (t * t * t)
    }

    /// কার্ভের tangent (দিক) বের করো
    pub fn tangent_at(&self, t: f32) -> Vec2 {
        let u = 1.0 - t;
        (self.p1 - self.p0) * (3.0 * u * u)
          + (self.p2 - self.p1) * (6.0 * u * t)
          + (self.p3 - self.p2) * (3.0 * t * t)
    }

    /// কার্ভকে সমতল রেখায় ভাগ করো (rendering এর জন্য)
    pub fn flatten(&self, tolerance: f32) -> Vec<Vec2> {
        let mut points = vec![self.p0];
        self.flatten_recursive(&mut points, tolerance, 0);
        points.push(self.p3);
        points
    }

    fn flatten_recursive(&self, points: &mut Vec<Vec2>, tolerance: f32, depth: u32) {
        if depth > 8 { return; }

        // চেক করো কার্ভ যথেষ্ট সমতল কিনা
        let midpoint = self.point_at(0.5);
        let chord_mid = (self.p0 + self.p3) * 0.5;
        let error = (midpoint - chord_mid).length();

        if error <= tolerance {
            points.push(midpoint);
        } else {
            // দুই ভাগে ভাগ করো (subdivision)
            let (left, right) = self.split(0.5);
            left.flatten_recursive(points, tolerance, depth + 1);
            right.flatten_recursive(points, tolerance, depth + 1);
        }
    }

    /// কার্ভকে দুই ভাগে ভাগ করো
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

/// 2D Vector
#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Vec2 {
    pub x: f32,
    pub y: f32,
}

impl Vec2 {
    pub fn new(x: f32, y: f32) -> Self { Self { x, y } }
    pub fn length(&self) -> f32 { (self.x*self.x + self.y*self.y).sqrt() }
    pub fn lerp(&self, other: Vec2, t: f32) -> Vec2 {
        Vec2::new(
            self.x + (other.x - self.x) * t,
            self.y + (other.y - self.y) * t,
        )
    }
}

impl std::ops::Add for Vec2 {
    type Output = Vec2;
    fn add(self, rhs: Vec2) -> Vec2 { Vec2::new(self.x + rhs.x, self.y + rhs.y) }
}

impl std::ops::Sub for Vec2 {
    type Output = Vec2;
    fn sub(self, rhs: Vec2) -> Vec2 { Vec2::new(self.x - rhs.x, self.y - rhs.y) }
}

impl std::ops::Mul<f32> for Vec2 {
    type Output = Vec2;
    fn mul(self, rhs: f32) -> Vec2 { Vec2::new(self.x * rhs, self.y * rhs) }
}
```

### SVG Parser

```rust
// src/formats/svg.rs — SVG ফাইল পার্সার

use std::collections::HashMap;

/// SVG Path ডেটা পার্স করো
pub fn parse_path_data(d: &str) -> Vec<PathCommand> {
    let mut commands = Vec::new();
    let mut chars = d.chars().peekable();
    let mut current_cmd = ' ';

    while let Some(&ch) = chars.peek() {
        match ch {
            'M' | 'm' => {
                chars.next();
                current_cmd = ch;
                let (x, y) = parse_coordinate_pair(&mut chars);
                commands.push(PathCommand::MoveTo { x, y, relative: ch.is_lowercase() });
            }
            'L' | 'l' => {
                chars.next();
                current_cmd = ch;
                let (x, y) = parse_coordinate_pair(&mut chars);
                commands.push(PathCommand::LineTo { x, y, relative: ch.is_lowercase() });
            }
            'C' | 'c' => {
                chars.next();
                current_cmd = ch;
                let (x1, y1) = parse_coordinate_pair(&mut chars);
                let (x2, y2) = parse_coordinate_pair(&mut chars);
                let (x, y) = parse_coordinate_pair(&mut chars);
                commands.push(PathCommand::CubicBezierTo {
                    x1, y1, x2, y2, x, y,
                    relative: ch.is_lowercase()
                });
            }
            'Z' | 'z' => {
                chars.next();
                commands.push(PathCommand::ClosePath);
            }
            ' ' | ',' | '\n' | '\t' => { chars.next(); }
            _ => { chars.next(); }
        }
    }

    commands
}

#[derive(Debug, Clone)]
pub enum PathCommand {
    MoveTo { x: f32, y: f32, relative: bool },
    LineTo { x: f32, y: f32, relative: bool },
    CubicBezierTo { x1: f32, y1: f32, x2: f32, y2: f32, x: f32, y: f32, relative: bool },
    ClosePath,
}

fn parse_coordinate_pair(chars: &mut std::iter::Peekable<std::str::Chars>) -> (f32, f32) {
    // whitespace skip
    while chars.peek() == Some(&' ') || chars.peek() == Some(&',') {
        chars.next();
    }
    let x = parse_number(chars);
    while chars.peek() == Some(&' ') || chars.peek() == Some(&',') {
        chars.next();
    }
    let y = parse_number(chars);
    (x, y)
}

fn parse_number(chars: &mut std::iter::Peekable<std::str::Chars>) -> f32 {
    let mut num_str = String::new();
    while let Some(&c) = chars.peek() {
        if c.is_ascii_digit() || c == '.' || c == '-' || c == '+' {
            num_str.push(c);
            chars.next();
        } else {
            break;
        }
    }
    num_str.parse().unwrap_or(0.0)
}
```

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
03-illustrator-alternative/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── geometry/
│   │   ├── bezier.rs       # Bezier curve math
│   │   ├── path.rs         # Path operations
│   │   └── boolean.rs      # Boolean operations (union, intersect)
│   ├── formats/
│   │   ├── svg.rs          # SVG read/write
│   │   ├── ai.rs           # Adobe AI reader (RE)
│   │   └── eps.rs          # EPS PostScript reader
│   ├── tools/
│   │   ├── pen.rs          # Pen tool
│   │   ├── selection.rs    # Selection tool
│   │   └── text.rs         # Type tool
│   └── ui/
│       └── canvas.rs       # Vector canvas
```

---

## 📚 রিসোর্স

- [SVG Specification (W3C)](https://www.w3.org/TR/SVG/)
- [Adobe PostScript Reference](https://www.adobe.com/products/postscript/pdfs/PLRM.pdf)
- [storytold/vectorcraft Reference](https://github.com/storytold/vectorcraft)
- [Inkscape Source Code](https://gitlab.com/inkscape/inkscape) — আরেকটি ভালো RE রেফারেন্স
