use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1440.0, 900.0])
            .with_title("FilmCraft — Open Source Premiere Pro"),
        ..Default::default()
    };
    eframe::run_native("FilmCraft", options, Box::new(|_cc| Ok(Box::new(FilmCraftApp::default()))))
}

#[derive(Default)]
struct FilmCraftApp {
    playhead_frame: i64,
    is_playing: bool,
    timeline_zoom: f32,
}

impl eframe::App for FilmCraftApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if self.is_playing {
            self.playhead_frame += 1;
            ctx.request_repaint();
        }

        egui::TopBottomPanel::top("menubar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("New Sequence…").clicked() { }
                    if ui.button("Import Media…").clicked() { }
                    if ui.button("Import PRPROJ…").clicked() { }
                    if ui.button("Export…").clicked() { }
                });
                ui.menu_button("Sequence", |ui| {
                    if ui.button("Sequence Settings…").clicked() { }
                    if ui.button("Render Timeline").clicked() { }
                });
                ui.menu_button("Clip", |ui| {
                    if ui.button("Speed/Duration…").clicked() { }
                    if ui.button("Unlink Audio/Video").clicked() { }
                });
            });
        });

        egui::TopBottomPanel::bottom("timeline").min_height(200.0).show(ctx, |ui| {
            ui.horizontal(|ui| {
                if ui.button("⏮").clicked() { self.playhead_frame = 0; }
                let play_label = if self.is_playing { "⏸" } else { "▶" };
                if ui.button(play_label).clicked() { self.is_playing = !self.is_playing; }
                if ui.button("⏭").clicked() { }
                ui.label(format!("Frame: {}", self.playhead_frame));
                ui.add(egui::Slider::new(&mut self.timeline_zoom, 0.1..=5.0).text("Zoom"));
            });
            ui.separator();
            ui.label("🎬 Timeline — V1 | V2 | A1 | A2");
            // Demo clip blocks
            for track in ["V2", "V1", "A1", "A2"] {
                ui.horizontal(|ui| {
                    ui.label(track);
                    let rect = egui::Rect::from_min_size(ui.cursor().min, egui::vec2(200.0, 20.0));
                    ui.painter().rect_filled(rect, 3.0, egui::Color32::from_rgb(70, 130, 180));
                    ui.allocate_rect(rect, egui::Sense::hover());
                });
            }
        });

        egui::SidePanel::left("media_bin").show(ctx, |ui| {
            ui.heading("Media Bin");
            ui.separator();
            for clip in ["intro.mp4", "interview.mov", "broll_1.mp4", "music.wav"] {
                ui.label(format!("🎬 {clip}"));
            }
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label("🖥️ Preview Monitor");
            let rect = ui.available_rect_before_wrap();
            ui.painter().rect_filled(rect.shrink(20.0), 4.0, egui::Color32::BLACK);
        });
    }
}
