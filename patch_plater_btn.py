import re

with open("src/slic3r/GUI/Plater.cpp", "r") as f:
    content = f.read()

pattern = r'(btn_pcb->Bind\(wxEVT_BUTTON, \[this, show_probharath_cnc_studio\]\(wxCommandEvent&\) \{ show_probharath_cnc_studio\(this->q, "pcb"\); \}\);\n\s*btn_metal->Bind\(wxEVT_BUTTON, \[this, show_probharath_cnc_studio\]\(wxCommandEvent&\) \{ show_probharath_cnc_studio\(this->q, "metal"\); \}\);)'

replacement = r'''btn_pcb->Bind(wxEVT_BUTTON, [main_frame](wxCommandEvent&) { main_frame->select_tab(TAB_ID_LIGHT_CNC); });
    btn_metal->Bind(wxEVT_BUTTON, [main_frame](wxCommandEvent&) { main_frame->select_tab(TAB_ID_HEAVY_CNC); });'''

content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/Plater.cpp", "w") as f:
    f.write(content)
