import re

with open("src/slic3r/GUI/MainFrame.cpp", "r") as f:
    content = f.read()

pattern = r'(auto panel_topbar = new wxPanel\(this, wxID_ANY\);\n\s*panel_topbar->SetBackgroundColour\(wxColour\(38, 46, 48\)\);\n\s*auto sizer_tobar = new wxBoxSizer\(wxVERTICAL\);\n\s*panel_topbar->SetSizer\(sizer_tobar\);\n\s*panel_topbar->Layout\(\);)'

replacement = r'''\1
    // ProBharath Mac Logo Injection
    wxString logo_path = wxString::FromUTF8(Slic3r::resources_dir() + "/images/probharath_elephant.png");
    wxImage logo_img;
    if (logo_img.LoadFile(logo_path, wxBITMAP_TYPE_PNG)) {
        logo_img.Rescale(FromDIP(48), FromDIP(48), wxIMAGE_QUALITY_HIGH);
        auto* logo_bmp = new wxStaticBitmap(panel_topbar, wxID_ANY, wxBitmap(logo_img));
        
        auto* h_sizer = new wxBoxSizer(wxHORIZONTAL);
        h_sizer->AddSpacer(15);
        h_sizer->Add(logo_bmp, 0, wxALIGN_CENTER_VERTICAL | wxTOP | wxBOTTOM, FromDIP(5));
        
        sizer_tobar->Add(h_sizer, 0, wxEXPAND);
        panel_topbar->Layout();
    }
'''

content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/MainFrame.cpp", "w") as f:
    f.write(content)
