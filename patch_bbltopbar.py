import re

with open("src/slic3r/GUI/BBLTopbar.cpp", "r") as f:
    content = f.read()

pattern = r'ProSlicer'
replacement = r'ProBharath'
content = re.sub(pattern, replacement, content)

with open("src/slic3r/GUI/BBLTopbar.cpp", "w") as f:
    f.write(content)
