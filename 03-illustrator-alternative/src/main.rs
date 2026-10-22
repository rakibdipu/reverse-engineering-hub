use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default()
            .with_inner_size([1280.0, 800.0])
            .with_title("VectorCraft — Open Source Illustrator"),
        ..Default::default()
    };
    eframe::run_native("VectorCraft", options, Box::new(|_cc| Ok(Box::new(VectorCraftApp::default()))))
}

#[derive(Default)]
struct VectorCraftApp {
    selected_tool: String,
    stroke_color: egui::Color32,
    fill_color: egui::Color32,
    stroke_width: f32,
}

impl eframe::App for VectorCraftApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::TopBottomPanel::top("menubar").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.menu_button("File", |ui| {
                    if ui.button("New…").clicked() { }
                    if ui.button("Open SVG…").clicked() { }
                    if ui.button("Open AI…").clicked() { }
                    if ui.button("Export SVG").clicked() { }
                    if ui.button("Export PDF").clicked() { }
                });
                ui.menu_button("Object", |ui| {
                    if ui.button("Group").clicked() { }
                    if ui.button("Ungroup").clicked() { }
                    if ui.button("Boolean Union").clicked() { }
                    if ui.button("Boolean Subtract").clicked() { }
                });
                ui.menu_button("Type", |ui| {
                    if ui.button("Create Outlines").clicked() { }
                    if ui.button("Text on Path").clicked() { }
                });
            });
        });

        egui::SidePanel::left("tools").show(ctx, |ui| {
            ui.label("✏️ Tools");
            ui.separator();
            for tool in ["Selection (V)", "Pen (P)", "Curvature (Shift+~)", "Type (T)",
                          "Rectangle (M)", "Ellipse (L)", "Star", "Rotate (R)", "Scale (S)"] {
                if ui.selectable_label(self.selected_tool == tool, tool).clicked() {
                    self.selected_tool = tool.to_string();
                }
            }
        });

        egui::TopBottomPanel::bottom("properties").show(ctx, |ui| {
            ui.horizontal(|ui| {
                ui.label("Stroke:");
                ui.color_edit_button_srgba(&mut self.stroke_color);
                ui.label("Fill:");
                ui.color_edit_button_srgba(&mut self.fill_color);
                ui.label("W:");
                ui.add(egui::Slider::new(&mut self.stroke_width, 0.0..=20.0));
            });
        });

        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label("🖊️ Vector canvas — click to place anchor, drag to curve");
            let (response, painter) = ui.allocate_painter(ui.available_size(), egui::Sense::click_and_drag());
            // Demo: draw a rectangle
            let rect = egui::Rect::from_min_size(response.rect.center() - egui::vec2(100.0, 60.0), egui::vec2(200.0, 120.0));
            painter.rect_stroke(rect, 4.0, egui::Stroke::new(2.0, egui::Color32::BLUE));
        });
    }
}
