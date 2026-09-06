from html import escape
from pathlib import Path

PALETTE = {"bg": "#0b0f14", "panel": "#111820", "line": "#263341", "text": "#e7edf3", "muted": "#8c9aaa", "accent": "#78dcca", "accent2": "#8aa9ff"}
FONT = "JetBrains Mono, ui-monospace, SFMono-Regular, Consolas, monospace"

def svg_open(width, height, title, desc=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">', f'<title id="title">{escape(title)}</title>', f'<desc id="desc">{escape(desc or title)}</desc>', f'<rect width="100%" height="100%" rx="14" fill="{PALETTE["bg"]}"/>']

def text(x, y, value, size=14, fill=None, weight="400", anchor="start"):
    return f'<text x="{x}" y="{y}" fill="{fill or PALETTE["text"]}" font-family="{FONT}" font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'

def finish(lines):
    lines.append('</svg>')
    return "\n".join(lines) + "\n"

def atomic_write(path, content):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    tmp.replace(path)
