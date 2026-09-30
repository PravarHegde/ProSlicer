import re

with open("src/slic3r/GUI/ParamsPanel.cpp", "r") as f:
    content = f.read()

# Let's add the wxChoice to the sizer instead of m_mode_view.
# Find where m_mode_view is added to the sizer:
pattern = r'm_mode_sizer->Add\(m_mode_view\s*,\s*0,\s*wxALIGN_CENTER\s*\|\s*wxRIGHT,\s*FromDIP\(SidebarProps::WideSpacing\(\)\)\);'

replacement = r'''
        // Hide the original custom drawing segmented button
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
        
        m_mode_sizer->Add(mode_combo, 0, wxALIGN_CENTER | wxRIGHT, FromDIP(SidebarProps::WideSpacing()));
'''

content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/ParamsPanel.cpp", "w") as f:
    f.write(content)
