import re

with open("src/slic3r/GUI/Plater.cpp", "r") as f:
    content = f.read()

pattern = r'(main_frame->select_tab\(TAB_ID_LIGHT_CNC\);\n\s*show_probharath_cnc_studio\(this->q, "pcb"\);)'
replacement = r'main_frame->select_tab(TAB_ID_LIGHT_CNC);'
content = re.sub(pattern, replacement, content)

pattern = r'(main_frame->select_tab\(TAB_ID_HEAVY_CNC\);\n\s*show_probharath_cnc_studio\(this->q, "metal"\);)'
replacement = r'main_frame->select_tab(TAB_ID_HEAVY_CNC);'
content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/Plater.cpp", "w") as f:
    f.write(content)
