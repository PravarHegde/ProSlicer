import re

with open("src/slic3r/GUI/MainFrame.cpp", "r") as f:
    content = f.read()

# Inside MainFrame::select_tab (approx line 4181)
pattern = r'(wxString new_selection = id\.empty\(\) \? m_last_selected_tab : id;\n\n        if \(m_tabpanel->GetSelectedPageName\(\) != new_selection\)\n            m_tabpanel->SelectPageByName\(new_selection\);)'

replacement = r'''\1
        if (m_param_panel) {
            if (id == TAB_ID_LIGHT_CNC) {
                m_param_panel->show_cnc_panel(true, "pcb");
            } else if (id == TAB_ID_HEAVY_CNC) {
                m_param_panel->show_cnc_panel(true, "metal");
            } else if (id == TAB_ID_PREPARE || id == TAB_ID_PREVIEW) {
                m_param_panel->show_cnc_panel(false, "");
            }
        }
'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("src/slic3r/GUI/MainFrame.cpp", "w") as f:
    f.write(content)
