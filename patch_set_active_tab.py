import re

with open("src/slic3r/GUI/ParamsPanel.cpp", "r") as f:
    content = f.read()

# 1. Update set_active_tab
pattern1 = r'(for \(auto t : std::vector<std::pair<wxPanel\*, wxStaticLine\*>>\(\{.*?\)\) \{\n\s*if \(!t\.first\) continue;\n\s*t\.first->Show\(tab == t\.first\);\n\s*if \(!t\.second\) continue;\n\s*t\.second->Show\(tab == t\.first\);\n\s*//m_left_sizer->GetItem\(t\)->SetProportion\(tab == t \? 1 : 0\);\n\s*\})'

replacement1 = r'''
    bool is_cnc_mode = m_cnc_panel && m_cnc_panel->IsShown();
    for (auto t : std::vector<std::pair<wxPanel*, wxStaticLine*>>({
            {m_tab_print, m_staticline_print},
            {m_tab_print_object, m_staticline_print_object},
            {m_tab_print_part, m_staticline_print_part},
            {m_tab_print_layer, nullptr},
            {m_tab_print_plate, nullptr},
            {m_tab_filament, m_staticline_filament},
            {m_tab_printer, m_staticline_printer}})) {
        if (!t.first) continue;
        t.first->Show(!is_cnc_mode && tab == t.first);
        if (!t.second) continue;
        t.second->Show(!is_cnc_mode && tab == t.first);
    }
'''

content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)

# 2. Update show_cnc_panel to call Layout
pattern2 = r'(m_cnc_panel->Show\(\);\n\s*\} else \{\n\s*m_cnc_panel->Hide\(\);)'
replacement2 = r'''\1'''

# Wait, let's just append m_left_sizer->Layout(); at the end of show_cnc_panel.
pattern3 = r'(if \(m_page_view\) m_page_view->Show\(\);\n\s*\})'
replacement3 = r'''\1
    
    if (m_left_sizer) {
        m_left_sizer->Layout();
    }
'''
content = re.sub(pattern3, replacement3, content)

with open("src/slic3r/GUI/ParamsPanel.cpp", "w") as f:
    f.write(content)
