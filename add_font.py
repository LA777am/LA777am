import urllib.request
import base64
import re

req = urllib.request.Request(
    'https://fonts.googleapis.com/css2?family=Press+Start+2P',
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
)
with urllib.request.urlopen(req) as response:
    css = response.read().decode('utf-8')

font_url = re.search(r'url\((https://[^)]+)\)', css).group(1)

with urllib.request.urlopen(font_url) as response:
    font_data = response.read()

b64_font = base64.b64encode(font_data).decode('utf-8')

with open('assets/header-wave.svg', 'r') as f:
    svg_content = f.read()

style_tag = f"""
    <style>
      @font-face {{
        font-family: 'Press Start 2P';
        src: url(data:font/woff2;charset=utf-8;base64,{b64_font}) format('woff2');
      }}
    </style>
"""
if '<style>' not in svg_content:
    svg_content = svg_content.replace('<defs>', '<defs>' + style_tag)

svg_content = re.sub(
    r'font-family="[^"]+"',
    'font-family="\'Press Start 2P\', monospace"',
    svg_content
)

# Press Start 2P might need a different font size to fit well
svg_content = re.sub(
    r'font-size="\d+"',
    'font-size="65"',
    svg_content
)

with open('assets/header-wave.svg', 'w') as f:
    f.write(svg_content)

print("Font injected successfully")
