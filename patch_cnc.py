import re

with open("src/slic3r/GUI/ParamsPanel.cpp", "r") as f:
    content = f.read()

# Append CNC Panel construction at the end of create_layout()
pattern = r'(m_top_sizer->Add\(m_left_sizer, 1, wxEXPAND\);\n\n.*m_left_sizer->AddSpacer\(6 \* em_unit\(this\) / 10\);)'

replacement = r'''\1
    
    // CNC Panel
    m_cnc_panel = new wxPanel(page_parent, wxID_ANY);
    m_cnc_panel->SetBackgroundColour(wxColour(18, 20, 26));
    auto* cnc_sizer = new wxBoxSizer(wxVERTICAL);
    
    auto* banner = new wxPanel(m_cnc_panel, wxID_ANY, wxDefaultPosition, wxSize(-1, 50));
    banner->SetBackgroundColour(wxColour(24, 28, 36));
    auto* banner_sizer = new wxBoxSizer(wxHORIZONTAL);
    auto* title_text = new wxStaticText(banner, wxID_ANY, _L("⚡ ProBharath CNC Studio"));
    title_text->SetForegroundColour(wxColour(0, 229, 255));
    title_text->SetFont(wxFont(13, wxFONTFAMILY_SWISS, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD));
    banner_sizer->AddSpacer(16);
    banner_sizer->Add(title_text, 0, wxALIGN_CENTER_VERTICAL);
    banner->SetSizer(banner_sizer);
    cnc_sizer->Add(banner, 0, wxEXPAND);
    
    auto* form_sizer = new wxFlexGridSizer(2, wxSize(14, 12));
    form_sizer->AddGrowableCol(1, 1);
    
    auto make_label = [this](const wxString& text) {
        auto* lbl = new wxStaticText(m_cnc_panel, wxID_ANY, text);
        lbl->SetForegroundColour(wxColour(220, 230, 245));
        lbl->SetFont(wxFont(10, wxFONTFAMILY_SWISS, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD));
        return lbl;
    };
    
    wxArrayString modes;
    modes.Add(_L("⚡ PCB Isolation Routing"));
    modes.Add(_L("🖋️ 2D Pen Plotting"));
    modes.Add(_L("🔩 Heavy Metal Milling"));
    auto* mode_choice = new wxChoice(m_cnc_panel, wxID_ANY, wxDefaultPosition, wxDefaultSize, modes);
    mode_choice->SetSelection(0);
    
    form_sizer->Add(make_label(_L("Operation:")), 0, wxALIGN_CENTER_VERTICAL);
    form_sizer->Add(mode_choice, 1, wxEXPAND);
    
    auto* tool_ctrl = new wxTextCtrl(m_cnc_panel, wxID_ANY, "0.10");
    form_sizer->Add(make_label(_L("Tool Tip Diameter (mm):")), 0, wxALIGN_CENTER_VERTICAL);
    form_sizer->Add(tool_ctrl, 1, wxEXPAND);
    
    auto* depth_ctrl = new wxTextCtrl(m_cnc_panel, wxID_ANY, "0.045");
    form_sizer->Add(make_label(_L("Cut Depth (mm):")), 0, wxALIGN_CENTER_VERTICAL);
    form_sizer->Add(depth_ctrl, 1, wxEXPAND);
    
    auto* rpm_ctrl = new wxTextCtrl(m_cnc_panel, wxID_ANY, "12000");
    form_sizer->Add(make_label(_L("Spindle (RPM):")), 0, wxALIGN_CENTER_VERTICAL);
    form_sizer->Add(rpm_ctrl, 1, wxEXPAND);
    
    auto* feed_ctrl = new wxTextCtrl(m_cnc_panel, wxID_ANY, "600");
    form_sizer->Add(make_label(_L("Feedrate (mm/min):")), 0, wxALIGN_CENTER_VERTICAL);
    form_sizer->Add(feed_ctrl, 1, wxEXPAND);
    
    cnc_sizer->AddSpacer(16);
    cnc_sizer->Add(form_sizer, 0, wxEXPAND | wxLEFT | wxRIGHT, 20);
    cnc_sizer->AddStretchSpacer(1);
    
    auto* gen_btn = new wxButton(m_cnc_panel, wxID_ANY, _L("⚡ Generate Toolpaths"), wxDefaultPosition, wxSize(-1, 34));
    gen_btn->SetBackgroundColour(wxColour(0, 102, 255));
    gen_btn->SetForegroundColour(wxColour(255, 255, 255));
    cnc_sizer->Add(gen_btn, 0, wxEXPAND | wxLEFT | wxRIGHT, 20);
    cnc_sizer->AddSpacer(20);
    
    m_cnc_panel->SetSizer(cnc_sizer);
    m_cnc_panel->Hide();
    
    m_top_sizer->Add(m_cnc_panel, 1, wxEXPAND);
'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Add show_cnc_panel
show_cnc_code = '''
void ParamsPanel::show_cnc_panel(bool show, const wxString& mode)
{
    if (!m_cnc_panel) return;
    
    if (show) {
#if __WXOSX__
        if (m_tmp_panel) m_tmp_panel->Hide();
#endif
        // Hiding the sizer's child by hiding the child directly doesn't always reflow,
        // but we can try just hiding elements and calling Layout()
        if (m_top_panel) m_top_panel->Hide();
        if (m_tab_print) m_tab_print->Hide();
        if (m_tab_filament) m_tab_filament->Hide();
        if (m_tab_printer) m_tab_printer->Hide();
        if (m_page_view) m_page_view->Hide();
        
        m_cnc_panel->Show();
    } else {
        m_cnc_panel->Hide();
#if __WXOSX__
        if (m_tmp_panel) m_tmp_panel->Show();
#endif
        if (m_top_panel) m_top_panel->Show();
        if (m_tab_print) m_tab_print->Show();
        if (m_tab_filament) m_tab_filament->Show();
        if (m_tab_printer) m_tab_printer->Show();
        if (m_page_view) m_page_view->Show();
    }
    
    m_top_sizer->Layout();
    Refresh();
}
'''

content += show_cnc_code

with open("src/slic3r/GUI/ParamsPanel.cpp", "w") as f:
    f.write(content)
