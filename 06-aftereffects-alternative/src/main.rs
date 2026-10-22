use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1440.0, 900.0])
            .with_title("EffectCraft — Open Source After Effects"),
        ..Default::default()
    };
    eframe::run_native("EffectCraft", options, Box::new(|_cc| Ok(Box::new(EffectCraftApp::default()))))
}

#[derive(Default)]
struct EffectCraftApp {
    current_time: f32,
    duration: f32,
    is_playing: bool,
    fps: f32,
    selected_layer: Option<usize>,
}

impl Default for EffectCraftApp {
    fn default() -> Self {
        Self { current_time: 0.0, duration: 10.0, is_playing: false, fps: 60.0, selected_layer: None }
    }
}

impl eframe::App for EffectCraftApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if self.is_playing {
            self.current_time += ctx.input(|i| i.stable_dt);
            if self.current_time >= self.duration { self.current_time = 0.0; }
            ctx.request_repaint();
        }

        egui::TopBottomPanel::top("menubar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("New Composition…").clicked() { }
                    if ui.button("Import AEP…").clicked() { }
                    if ui.button("Export…").clicked() { }
                    if ui.button("Add to Render Queue").clicked() { }
                });
                ui.menu_button("Layer", |ui| {
                    if ui.button("New Solid…").clicked() { }
                    if ui.button("New Shape Layer").clicked() { }
                    if ui.button("New Text Layer").clicked() { }
                    if ui.button("New Null Object").clicked() { }
                    if ui.button("New Camera…").clicked() { }
                    if ui.button("New Light…").clicked() { }
                });
                ui.menu_button("Effect", |ui| {
                    ui.menu_button("Blur & Sharpen", |ui| {
                        if ui.button("Gaussian Blur").clicked() { }
                        if ui.button("Camera Lens Blur").clicked() { }
                    });
                    ui.menu_button("Color Correction", |ui| {
                        if ui.button("Curves").clicked() { }
                        if ui.button("Levels").clicked() { }
                        if ui.button("Hue/Saturation").clicked() { }
                    });
                    ui.menu_button("Distort", |ui| {
                        if ui.button("Warp").clicked() { }
                        if ui.button("Turbulent Displace").clicked() { }
                    });
                });
            });
        });

        egui::TopBottomPanel::bottom("timeline").min_height(220.0).show(ctx, |ui| {
            ui.horizontal(|ui| {
                if ui.button("⏮").clicked() { self.current_time = 0.0; }
                let play_label = if self.is_playing { "⏸" } else { "▶" };
                if ui.button(play_label).clicked() { self.is_playing = !self.is_playing; }
                if ui.button("⏭").clicked() { self.current_time = self.duration; }
                ui.label(format!("{:.2}s / {:.1}s  @{:.0}fps", self.current_time, self.duration, self.fps));
            });
            ui.separator();

            let layers = ["🟩 Solid (BG)", "📝 Text Layer", "🟠 Shape Layer", "📷 Camera", "💡 Light"];
            for (i, layer) in layers.iter().enumerate() {
                ui.horizontal(|ui| {
                    let selected = self.selected_layer == Some(i);
                    if ui.selectable_label(selected, format!("{:>24}", layer)).clicked() {
                        self.selected_layer = Some(i);
                    }
                    let avail = ui.available_width();
                    let rect = egui::Rect::from_min_size(ui.cursor().min, egui::vec2(avail, 18.0));
                    let color = egui::Color32::from_rgb(60 + (i as u8 * 30), 100, 180);
                    ui.painter().rect_filled(rect, 2.0, color);
                    ui.allocate_rect(rect, egui::Sense::hover());
                });
            }
        });

        egui::SidePanel::left("project_panel").show(ctx, |ui| {
            ui.heading("Project");
            for item in ["📦 Compositions", "🎬 Footage", "📝 Solids", "🔤 Fonts"] {
                ui.label(item);
            }
            ui.separator();
            ui.heading("Effects & Presets");
            for fx in ["Gaussian Blur", "Curves", "Levels", "Glow", "Turbulent Displace"] {
                ui.label(format!("✨ {fx}"));
            }
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label("🖥️ Composition Preview");
            let rect = ui.available_rect_before_wrap().shrink(10.0);
            ui.painter().rect_filled(rect, 4.0, egui::Color32::BLACK);
        });
    }
}
