import re

with open("src/slic3r/GUI/ParamsPanel.cpp", "r") as f:
    content = f.read()

pattern = r'(cnc_sizer->Add\(gen_btn, 0, wxEXPAND \| wxLEFT \| wxRIGHT, 20\);\n\s*cnc_sizer->AddSpacer\(20\);)'
replacement = r'''\1
    
    gen_btn->Bind(wxEVT_BUTTON, [this](wxCommandEvent&) {
        if (wxGetApp().plater() && wxGetApp().plater()->get_notification_manager()) {
            wxGetApp().plater()->get_notification_manager()->push_notification(
                into_u8(_L("⚡ ProBharath AI CAM: Calculating optimal subtractive multi-axis toolpaths in background...")));
        }
    });
'''

content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/ParamsPanel.cpp", "w") as f:
    f.write(content)
