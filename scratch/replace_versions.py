import os
import re

directories = ["src", "CMakeLists.txt", "version.inc"]

replacements = {
    "SoftFever_VERSION": "PROBHARATH_VERSION",
    "ORCA_VERSION_MAJOR": "PROBHARATH_VERSION_MAJOR",
    "ORCA_VERSION_MINOR": "PROBHARATH_VERSION_MINOR",
    "ORCA_VERSION_PATCH": "PROBHARATH_VERSION_PATCH",
    "orca_version": "probharath_version"
}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files
    
    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for path in directories:
    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                process_file(os.path.join(root, file))

print("Done replacing version strings.")
