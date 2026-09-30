import re

with open("src/slic3r/GUI/Tab.cpp", "r") as f:
    content = f.read()

pattern = r'(m_top_sizer->Add\( m_mode_view, 0, wxALIGN_CENTER_VERTICAL\);)'
replacement = r'''
        m_mode_view->Hide();
        
        wxArrayString mode_strings;
        mode_strings.Add(_L("Standard (Basic)"));
        mode_strings.Add(_L("Advanced Settings"));
        mode_strings.Add(_L("Expert (All Features)"));
        auto* mode_combo = new wxChoice(m_top_panel, wxID_ANY, wxDefaultPosition, wxDefaultSize, mode_strings);
        mode_combo->SetSelection(m_mode_view->GetSelection());
        
        mode_combo->Bind(wxEVT_CHOICE, [this](wxCommandEvent& e) {
            if (m_mode_view) {
                m_mode_view->SelectAndNotify(e.GetSelection());
            }
        });
        
        m_top_sizer->Add(mode_combo, 0, wxALIGN_CENTER_VERTICAL);
'''

content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/Tab.cpp", "w") as f:
    f.write(content)
