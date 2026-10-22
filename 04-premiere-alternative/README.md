# 🎬 Project 04: FilmCraft — Adobe Premiere Pro বিকল্প

> **Rust + WebGPU দিয়ে তৈরি ওপেন-সোর্স Non-Linear Video Editor (NLE)**

[![Reference](https://img.shields.io/badge/Inspired%20By-storytold%2Ffilmcraft-blue)](https://github.com/storytold/filmcraft)

---

## 📖 কী এটা?

**FilmCraft** হলো Adobe Premiere Pro-এর একটি বিকল্প যা:
- **Adobe Premiere (`.prproj`)** প্রজেক্ট ফাইল রিড করতে পারে
- **Timeline-based** ভিডিও এডিটিং সাপোর্ট করে
- **FFmpeg** ব্যবহার করে সব ফরম্যাট সাপোর্ট করে
- **GPU-accelerated** রেন্ডারিং (WebGPU/wgpu)

---

## 🔬 Adobe Premiere PRPROJ Format — RE Analysis

Premiere Pro-এর `.prproj` ফাইল আসলে একটি **gzipped XML** ফাইল:

```bash
# PRPROJ ফাইল কী সেটা দেখুন
file project.prproj
# Output: project.prproj: gzip compressed data

# Decompress করুন
cp project.prproj project.prproj.gz
gunzip project.prproj.gz
file project.prproj
# Output: project.prproj: XML document, ASCII text

# XML দেখুন
cat project.prproj | head -50
```

### PRPROJ XML Structure (RE করা)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PremiereData Version="3">
  <!-- Project Settings -->
  <ProjectSettings>
    <VideoSettings>
      <FrameRate>
        <TimeBase>25</TimeBase>  <!-- 25fps -->
      </FrameRate>
      <FrameWidth>1920</FrameWidth>
      <FrameHeight>1080</FrameHeight>
    </VideoSettings>
  </ProjectSettings>

  <!-- Media Items (Clips) -->
  <Media>
    <ProjectItem ObjectID="1" ClassID="62ad66dd-...">
      <Name>footage.mp4</Name>
      <FilePath>C:\Videos\footage.mp4</FilePath>
      <MediaType>Video</MediaType>
      <Duration>
        <TimeBase>25</TimeBase>
        <Time>250</Time>  <!-- 10 seconds at 25fps -->
      </Duration>
    </ProjectItem>
  </Media>

  <!-- Sequences (Timeline) -->
  <Sequence ObjectID="5">
    <Name>Sequence 01</Name>
    <Duration>...</Duration>
    <VideoTracks>
      <Track>
        <ClipItem>
          <Link>1</Link>  <!-- Media item reference -->
          <Start>0</Start>
          <End>100</End>
          <InPoint>0</InPoint>
          <OutPoint>100</OutPoint>
        </ClipItem>
      </Track>
    </VideoTracks>
    <AudioTracks>
      <!-- Audio track clips -->
    </AudioTracks>
  </Sequence>
</PremiereData>
```

---

## 🦀 Rust Implementation

```rust
// src/formats/prproj.rs — Premiere Pro project reader

use serde::Deserialize;

/// Premiere Pro প্রজেক্ট ডেটা
#[derive(Debug, Deserialize)]
#[serde(rename = "PremiereData")]
pub struct PremiereProject {
    #[serde(rename = "Version")]
    pub version: String,

    #[serde(rename = "ProjectSettings")]
    pub settings: Option<ProjectSettings>,

    #[serde(rename = "Sequence", default)]
    pub sequences: Vec<Sequence>,
}

#[derive(Debug, Deserialize)]
pub struct ProjectSettings {
    #[serde(rename = "VideoSettings")]
    pub video: VideoSettings,
}

#[derive(Debug, Deserialize)]
pub struct VideoSettings {
    #[serde(rename = "FrameWidth")]
    pub width: u32,
    #[serde(rename = "FrameHeight")]
    pub height: u32,
}

#[derive(Debug, Deserialize)]
pub struct Sequence {
    #[serde(rename = "Name")]
    pub name: String,
    #[serde(rename = "VideoTracks")]
    pub video_tracks: Option<VideoTracks>,
}

#[derive(Debug, Deserialize)]
pub struct VideoTracks {
    #[serde(rename = "Track", default)]
    pub tracks: Vec<Track>,
}

#[derive(Debug, Deserialize)]
pub struct Track {
    #[serde(rename = "ClipItem", default)]
    pub clips: Vec<ClipItem>,
}

#[derive(Debug, Deserialize)]
pub struct ClipItem {
    #[serde(rename = "Name")]
    pub name: Option<String>,
    #[serde(rename = "Start")]
    pub start: i64,
    #[serde(rename = "End")]
    pub end: i64,
}

/// PRPROJ ফাইল লোড করো
pub fn load_prproj(path: &str) -> Result<PremiereProject, Box<dyn std::error::Error>> {
    use std::io::Read;
    use flate2::read::GzDecoder;

    // gzip decompress
    let file = std::fs::File::open(path)?;
    let mut decoder = GzDecoder::new(file);
    let mut xml = String::new();
    decoder.read_to_string(&mut xml)?;

    // XML parse
    let project: PremiereProject = quick_xml::de::from_str(&xml)?;
    Ok(project)
}
```

---

## 🎬 Timeline Engine

```rust
// src/timeline/mod.rs — NLE Timeline

/// Timeline-এর একটি clip
#[derive(Debug, Clone)]
pub struct TimelineClip {
    pub id: u64,
    pub source_path: String,
    pub track: u32,
    pub start_frame: i64,    // Timeline-এ কোথায় শুরু
    pub end_frame: i64,      // Timeline-এ কোথায় শেষ
    pub in_point: i64,       // Source clip-এর কোথা থেকে শুরু
    pub out_point: i64,      // Source clip-এর কোথায় শেষ
}

/// Timeline State
pub struct Timeline {
    pub clips: Vec<TimelineClip>,
    pub current_frame: i64,
    pub total_frames: i64,
    pub frame_rate: f32,
}

impl Timeline {
    pub fn new(frame_rate: f32) -> Self {
        Self {
            clips: Vec::new(),
            current_frame: 0,
            total_frames: 0,
            frame_rate,
        }
    }

    /// একটি clip যোগ করো
    pub fn add_clip(&mut self, clip: TimelineClip) {
        self.total_frames = self.total_frames.max(clip.end_frame);
        self.clips.push(clip);
    }

    /// নির্দিষ্ট frame-এ কোন clips active আছে?
    pub fn clips_at_frame(&self, frame: i64) -> Vec<&TimelineClip> {
        self.clips.iter()
            .filter(|c| frame >= c.start_frame && frame < c.end_frame)
            .collect()
    }

    /// Timeline seconds থেকে frames এ convert
    pub fn seconds_to_frames(&self, seconds: f32) -> i64 {
        (seconds * self.frame_rate) as i64
    }
}
```

---

## 📁 প্রজেক্ট স্ট্রাকচার

```
04-premiere-alternative/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── formats/
│   │   ├── prproj.rs      # Premiere Pro project reader
│   │   └── fcpxml.rs      # Final Cut Pro XML reader
│   ├── timeline/
│   │   ├── mod.rs         # Timeline state
│   │   ├── clip.rs        # Clip management
│   │   └── effects.rs     # Video effects
│   ├── decoder/
│   │   └── ffmpeg.rs      # FFmpeg wrapper
│   ├── renderer/
│   │   └── gpu.rs         # WebGPU renderer
│   └── ui/
│       ├── timeline_view.rs
│       └── preview.rs
└── Cargo.lock
```

---

## 📚 রিসোর্স

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [wgpu (Rust WebGPU)](https://wgpu.rs/)
- [storytold/filmcraft Reference](https://github.com/storytold/filmcraft)
- [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO)
