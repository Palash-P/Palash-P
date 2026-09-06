import argparse, math
from pathlib import Path
from xml.sax.saxutils import escape

RAMP = " .`:-=+*cs#%@"

def render(args):
    try:
        from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    except ImportError as exc:
        raise SystemExit("Portrait generation requires Pillow: pip install Pillow") from exc
    source = Path(args.input)
    if not source.is_file(): raise SystemExit(f"Portrait not found: {source}")
    image = Image.open(source).convert("RGB")
    ratio = image.height / image.width
    rows = max(1, round(args.columns * ratio * args.char_ratio))
    image = ImageOps.fit(image, (args.columns, rows), method=Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.BILATERAL if hasattr(ImageFilter, "BILATERAL") else ImageFilter.GaussianBlur(.35))
    image = ImageOps.grayscale(image)
    image = ImageEnhance.Contrast(image).enhance(args.contrast)
    pixels = list(image.getdata())
    chars = [RAMP[min(len(RAMP)-1, int(((p/255) ** args.gamma) * (len(RAMP)-1)))] for p in pixels]
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {args.columns*7.74:.2f} {rows*15:.2f}" role="img" aria-labelledby="title desc">', '<title id="title">Palash Pingale portrait rendered as ASCII</title>', '<desc id="desc">A monochrome animated ASCII portrait.</desc>', '<rect width="100%" height="100%" fill="#0b0f14"/>']
    for row in range(rows):
        value = escape(''.join(chars[row*args.columns:(row+1)*args.columns]))
        y = 13 + row * 15
        lines.append(f'<clipPath id="r{row}"><rect x="0" y="{row*15}" width="0" height="15"><animate attributeName="width" from="0" to="{args.columns*7.74:.2f}" dur="0.8s" begin="{row*0.04:.2f}s" fill="freeze"/></rect></clipPath>')
        lines.append(f'<text x="0" y="{y}" fill="#78dcca" font-family="JetBrains Mono, monospace" font-size="12.9px" xml:space="preserve" clip-path="url(#r{row})"><tspan>{value}</tspan></text>')
    lines.append('</svg>')
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True); out.write_text("\n".join(lines)+"\n", encoding="utf-8")

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--input", required=True); p.add_argument("--output", required=True); p.add_argument("--columns", type=int, default=72); p.add_argument("--char-ratio", type=float, default=.48); p.add_argument("--contrast", type=float, default=1.35); p.add_argument("--gamma", type=float, default=1.7); render(p.parse_args())
