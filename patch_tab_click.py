import re

with open("src/slic3r/GUI/MainFrame.cpp", "r") as f:
    content = f.read()

pattern = r'(else if \(m_last_selected_tab == TAB_ID_PREVIEW\) \{\n\s*m_plater->reset_check_status\(\);\n\s*if \(!m_plater->check_ams_status\(m_slice_select == eSliceAll\)\)\n\s*return;\n\s*wxPostEvent\(m_plater, SimpleEvent\(EVT_GLVIEWTOOLBAR_PREVIEW\)\);\n\s*m_param_panel->OnActivate\(\);\n\s*\})'

replacement = r'''\1
            else if (m_last_selected_tab == TAB_ID_LIGHT_CNC) {
                wxPostEvent(m_plater, SimpleEvent(EVT_GLVIEWTOOLBAR_3D));
                m_param_panel->OnActivate();
                m_param_panel->show_cnc_panel(true, "pcb");
            }
            else if (m_last_selected_tab == TAB_ID_HEAVY_CNC) {
                wxPostEvent(m_plater, SimpleEvent(EVT_GLVIEWTOOLBAR_3D));
                m_param_panel->OnActivate();
                m_param_panel->show_cnc_panel(true, "metal");
            }
'''

content = re.sub(pattern, replacement, content)

# We should also ensure that when switching BACK to Prepare, show_cnc_panel(false) is called
pattern2 = r'(if \(m_last_selected_tab == TAB_ID_PREPARE\) \{\n\s*wxPostEvent\(m_plater, SimpleEvent\(EVT_GLVIEWTOOLBAR_3D\)\);\n\s*m_param_panel->OnActivate\(\);\n\s*\})'

replacement2 = r'''if (m_last_selected_tab == TAB_ID_PREPARE) {
                wxPostEvent(m_plater, SimpleEvent(EVT_GLVIEWTOOLBAR_3D));
                m_param_panel->OnActivate();
                m_param_panel->show_cnc_panel(false, "");
            }'''

content = re.sub(pattern2, replacement2, content)

with open("src/slic3r/GUI/MainFrame.cpp", "w") as f:
    f.write(content)
