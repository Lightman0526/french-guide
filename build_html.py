import re
import markdown

file_path = 'Travel_Guide.md'
output_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

# 1. Process images spaces
md_text = md_text.replace('Pasted image ', 'Pasted%20image%20')

# 2. Process Checkboxes
md_text = md_text.replace('- [ ]', '- <input type="checkbox" disabled>')
md_text = md_text.replace('- [x]', '- <input type="checkbox" checked disabled>')

# 3. Process Callouts
def replacer(match):
    ctype = match.group(1).lower()
    title = match.group(2).strip()
    content = match.group(3)
    content = re.sub(r'^>\s?', '', content, flags=re.MULTILINE)
    
    type_map = {
        'info': 'alert-info',
        'tip': 'alert-tip',
        'warning': 'alert-warning',
        'danger': 'alert-danger',
        'error': 'alert-danger',
        'important': 'alert-info'
    }
    css_class = type_map.get(ctype, 'alert-info')
    
    return f'<div class="alert {css_class}"><div class="alert-title">{title}</div><div class="alert-content" markdown="1">\n\n{content}\n\n</div></div>'

pattern = re.compile(r'^> \[!(\w+)\](.*?)\n((?:>.*\n?)*)', re.MULTILINE)
md_text = pattern.sub(replacer, md_text)

# Convert Markdown to HTML
html_content = markdown.markdown(md_text, extensions=['tables', 'md_in_html'])

# Build final HTML
html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 法国夏日探索指南</title>
    <style>
    :root {{
        --primary-color: #2c3e50;
        --bg-color: #f8f9fa;
        --border-color: #e1e4e8;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        line-height: 1.6;
        color: #24292e;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: var(--bg-color);
    }}
    h1, h2, h3 {{
        color: var(--primary-color);
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 10px;
        margin-top: 1.5em;
    }}
    img {{
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
        overflow-x: auto;
        display: block;
    }}
    th, td {{
        border: 1px solid var(--border-color);
        padding: 12px;
        text-align: left;
    }}
    th {{ background-color: #f6f8fa; }}
    blockquote {{
        margin: 0;
        padding: 10px 20px;
        color: #6a737d;
        border-left: 0.25em solid var(--border-color);
        background: #fff;
    }}
    input[type="checkbox"] {{
        margin-right: 10px;
        transform: scale(1.2);
    }}
    a {{
        color: #0366d6;
        text-decoration: none;
    }}
    .alert {{
        border-radius: 6px;
        border-left: 6px solid;
        margin: 20px 0;
        padding: 15px;
        background: #fff;
    }}
    .alert-title {{
        font-weight: bold;
        margin-bottom: 8px;
    }}
    .alert-info {{ border-left-color: #0366d6; background: #f1f8ff; }}
    .alert-tip {{ border-left-color: #28a745; background: #f0fff4; }}
    .alert-warning {{ border-left-color: #ffd33d; background: #fffdef; }}
    .alert-danger {{ border-left-color: #d73a49; background: #ffeef0; }}
    
    @media (max-width: 600px) {{
        body {{ padding: 15px; }}
        h1 {{ font-size: 1.5em; }}
    }}
    
    li {{ margin-bottom: 8px; }}
    li:has(input[type="checkbox"]) {{
        list-style-type: none;
        margin-left: -24px;
    }}
    p:has(img) {{
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        justify-content: center;
        align-items: center;
    }}
    p:has(img) img {{ margin: 0; }}
    img[src*="unsplash"] {{
        width: 100%;
        object-fit: cover;
    }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_template)

print("index.html rebuilt successfully!")
