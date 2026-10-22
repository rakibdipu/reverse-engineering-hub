use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1440.0, 900.0])
            .with_title("LightCraft — Open Source Lightroom"),
        ..Default::default()
    };
    eframe::run_native("LightCraft", options, Box::new(|_cc| Ok(Box::new(LightCraftApp::default()))))
}

#[derive(Default)]
struct LightCraftApp {
    exposure: f32,
    contrast: f32,
    highlights: f32,
    shadows: f32,
    whites: f32,
    blacks: f32,
    temperature: f32,
    tint: f32,
    saturation: f32,
    clarity: f32,
    vibrance: f32,
    sharpening: f32,
    noise_reduction: f32,
}

impl eframe::App for LightCraftApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::TopBottomPanel::top("menubar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("Import LRCAT Catalog…").clicked() { }
                    if ui.button("Import RAW Photos…").clicked() { }
                    if ui.button("Export with Settings…").clicked() { }
                });
                ui.selectable_label(true, "Library");
                ui.selectable_label(false, "Develop");
                ui.selectable_label(false, "Map");
                ui.selectable_label(false, "Book");
                ui.selectable_label(false, "Slideshow");
                ui.selectable_label(false, "Print");
                ui.selectable_label(false, "Web");
            });
        });

        egui::SidePanel::right("develop_panel").min_width(250.0).show(ctx, |ui| {
            ui.heading("Develop");
            ui.separator();
            ui.collapsing("Basic", |ui| {
                ui.label("White Balance");
                ui.add(egui::Slider::new(&mut self.temperature, 2000.0..=50000.0).text("Temp (K)"));
                ui.add(egui::Slider::new(&mut self.tint, -150.0..=150.0).text("Tint"));
                ui.separator();
                ui.label("Tone");
                ui.add(egui::Slider::new(&mut self.exposure, -5.0..=5.0).text("Exposure"));
                ui.add(egui::Slider::new(&mut self.contrast, -100.0..=100.0).text("Contrast"));
                ui.add(egui::Slider::new(&mut self.highlights, -100.0..=100.0).text("Highlights"));
                ui.add(egui::Slider::new(&mut self.shadows, -100.0..=100.0).text("Shadows"));
                ui.add(egui::Slider::new(&mut self.whites, -100.0..=100.0).text("Whites"));
                ui.add(egui::Slider::new(&mut self.blacks, -100.0..=100.0).text("Blacks"));
                ui.separator();
                ui.label("Presence");
                ui.add(egui::Slider::new(&mut self.saturation, -100.0..=100.0).text("Saturation"));
                ui.add(egui::Slider::new(&mut self.vibrance, -100.0..=100.0).text("Vibrance"));
                ui.add(egui::Slider::new(&mut self.clarity, -100.0..=100.0).text("Clarity"));
            });
            ui.collapsing("Detail", |ui| {
                ui.add(egui::Slider::new(&mut self.sharpening, 0.0..=150.0).text("Sharpening"));
                ui.add(egui::Slider::new(&mut self.noise_reduction, 0.0..=100.0).text("Noise Reduction"));
            });
        });

        egui::SidePanel::left("film_strip").show(ctx, |ui| {
            ui.heading("Library");
            for i in 1..=8 {
                let rect = egui::Rect::from_min_size(ui.cursor().min, egui::vec2(160.0, 100.0));
                ui.painter().rect_filled(rect, 4.0, egui::Color32::DARK_GRAY);
                ui.label(format!("IMG_{:04}.CR3", i * 1000));
                ui.add_space(4.0);
            }
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label("📷 RAW Preview — adjustments applied in real time");
            let rect = ui.available_rect_before_wrap().shrink(10.0);
            ui.painter().rect_filled(rect, 8.0, egui::Color32::from_gray(30));
        });
    }
}
