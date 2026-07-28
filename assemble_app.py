import json

with open('app_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

briefs_json_str = json.dumps(data['briefs'], ensure_ascii=False)
sources_json_str = json.dumps(data['data_sources'], ensure_ascii=False)

with open('app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

target_marker = '<script id="briefs-data"'
marker_pos = html_content.find(target_marker)

base_html = html_content[:marker_pos]

final_html = base_html + f"""<script id="briefs-data" type="application/json">
{briefs_json_str}
</script>
<script id="sources-data" type="application/json">
{sources_json_str}
</script>

<script>
{js_content}
</script>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

with open('3MTT_NextGen_Project_Brief_Bank.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Assembled standalone HTML successfully!")
