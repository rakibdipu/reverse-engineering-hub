use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1280.0, 800.0])
            .with_title("PhotoCraft — Open Source Photoshop"),
        ..Default::default()
    };
    eframe::run_native("PhotoCraft", options, Box::new(|_cc| Ok(Box::new(PhotoCraftApp::default()))))
}

#[derive(Default)]
struct PhotoCraftApp {
    canvas_width: u32,
    canvas_height: u32,
    zoom: f32,
}

impl eframe::App for PhotoCraftApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::TopBottomPanel::top("menubar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("New…").clicked() { }
                    if ui.button("Open PSD…").clicked() { }
                    if ui.button("Save As PNG").clicked() { }
                    if ui.button("Export…").clicked() { }
                });
                ui.menu_button("Image", |ui| {
                    if ui.button("Canvas Size…").clicked() { }
                    if ui.button("Image Size…").clicked() { }
                    if ui.button("Rotate…").clicked() { }
                });
                ui.menu_button("Layer", |ui| {
                    if ui.button("New Layer").clicked() { }
                    if ui.button("Merge Down").clicked() { }
                    if ui.button("Flatten Image").clicked() { }
                });
                ui.menu_button("Filter", |ui| {
                    if ui.button("Gaussian Blur…").clicked() { }
                    if ui.button("Sharpen").clicked() { }
                    if ui.button("Noise…").clicked() { }
                });
            });
        });

        egui::SidePanel::left("tools").show(ctx, |ui| {
            ui.label("🖌️ Tools");
            ui.separator();
            let tools = ["Move (V)", "Lasso (L)", "Brush (B)", "Eraser (E)",
                          "Clone Stamp (S)", "Eyedropper (I)", "Crop (C)", "Text (T)"];
            for tool in tools {
                ui.selectable_label(false, tool);
            }
        });

        egui::SidePanel::right("layers").min_width(200.0).show(ctx, |ui| {
            ui.heading("Layers");
            ui.separator();
            for i in (1..=4).rev() {
                ui.horizontal(|ui| {
                    ui.label(format!("👁 Layer {i}"));
                });
            }
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label("🎨 Canvas — drag to pan, scroll to zoom");
            ui.add(egui::Slider::new(&mut self.zoom, 0.1..=8.0).text("Zoom"));
        });
    }
}
