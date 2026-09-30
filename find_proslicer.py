import os
import re

found = 0
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.cpp') or file.endswith('.hpp') or file.endswith('.h') or file.endswith('.js') or file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    matches = re.findall(r'.{0,30}ProSlicer.{0,30}', content, flags=re.IGNORECASE)
                    for match in matches:
                        print(f"{filepath}: {match.strip()}")
                        found += 1
                        if found > 20:
                            exit(0)
            except Exception:
                pass
