import re
import markdown

with open("Travel_Guide.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Replace checkboxes
md_content = md_content.replace("- [x] ", "- <input type=\"checkbox\" checked disabled> ")
md_content = md_content.replace("- [ ] ", "- <input type=\"checkbox\" disabled> ")

# Process alerts
lines = md_content.split('\n')
new_lines = []
in_alert = False

for line in lines:
    if line.startswith("> [!"):
        match = re.match(r'> \[!(.*?)\] (.*)', line)
        if match:
            alert_type = match.group(1).lower()
            title = match.group(2)
            new_lines.append(f'<div class="alert alert-{alert_type}"><div class="alert-title">{title}</div><div class="alert-content">\n')
            in_alert = True
        else:
            new_lines.append(line)
    elif in_alert and line.startswith(">"):
        # remove the leading '>' and space
        new_lines.append(line[1:].lstrip())
    elif in_alert and not line.startswith(">"):
        if line.strip() == "":
            new_lines.append("\n</div></div>\n")
            new_lines.append(line)
            in_alert = False
        else:
            new_lines.append("\n</div></div>\n")
            new_lines.append(line)
            in_alert = False
    else:
        new_lines.append(line)

if in_alert:
    new_lines.append("\n</div></div>\n")

md_processed = '\n'.join(new_lines)

try:
    # Try with md_in_html
    html_body = markdown.markdown(md_processed, extensions=['tables', 'md_in_html'])
except:
    # Fallback
    html_body = markdown.markdown(md_processed, extensions=['tables'])

with open("index.html", "r", encoding="utf-8") as f:
    old_html = f.read()

head_part = old_html.split("</head>")[0] + "</head>\n<body>\n"

full_html = head_part + html_body + "\n</body>\n</html>"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("Done")
