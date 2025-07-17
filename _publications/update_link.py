import os
import re

def convert_links_to_html(text):
    # Match [text](url)
    return re.sub(r'\[([^\]]+)\]\((http[s]?://[^\)]+)\)', r'<a href="\2">\1</a>', text)

for root, _, files in os.walk('.'):
    for filename in files:
        if filename.endswith('.md') or filename.endswith('.markdown'):
            path = os.path.join(root, filename)
            with open(path, encoding='utf-8') as f:
                content = f.read()

            if 'citation:' in content:
                updated = convert_links_to_html(content)
                if updated != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(updated)
                    print(f"Updated links in {path}")
