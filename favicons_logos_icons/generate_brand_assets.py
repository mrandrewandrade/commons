#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import cairosvg
import math
import ezdxf
from svgpathtools import svg2paths2

ROOT = Path(__file__).resolve().parents[1] / "site" / "assets" / "branding"
LOGO = ROOT / "logo"
EMBLEM = ROOT / "emblem"
NAVY = "#062650"
CREAM = "#FAF7F2"
BLACK = "#111111"


def render_svg(svg_path: Path, png_path: Path, width: int, height: int | None = None, background: str | None = None):
    height = height or width
    tmp = png_path.with_suffix(png_path.suffix + ".tmp")
    cairosvg.svg2png(url=str(svg_path), write_to=str(tmp), output_width=width, output_height=height)
    image = Image.open(tmp).convert("RGBA")
    tmp.unlink()
    if background:
        base = Image.new("RGBA", image.size, background)
        base.alpha_composite(image)
        image = base.convert("RGB")
    image.save(png_path)


def svg_to_dxf(svg_path: Path, dxf_path: Path, sample_step: float = 4.0):
    """Convert SVG vector paths to fabrication-friendly DXF polylines."""
    paths, _, _ = svg2paths2(str(svg_path))
    doc = ezdxf.new(setup=True)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for path in paths:
        for subpath in path.continuous_subpaths():
            if len(subpath) == 0:
                continue
            points = []
            for segment in subpath:
                try:
                    length = max(float(segment.length(error=1e-4)), sample_step)
                except Exception:
                    length = sample_step
                samples = max(2, int(math.ceil(length / sample_step)) + 1)
                for i in range(samples):
                    if points and i == 0:
                        continue
                    z = segment.point(i / (samples - 1))
                    points.append((float(z.real), float(-z.imag)))
            if len(points) >= 2:
                is_closed = abs(subpath.start - subpath.end) < 1e-6
                msp.add_lwpolyline(points, close=is_closed)
    doc.saveas(dxf_path)


def icon_from_aa(size: int, background=None, white_mark=False):
    source = LOGO / ("aa-logo-white.svg" if white_mark else "aa-logo.svg")
    tmp = LOGO / ".aa-icon-tmp.png"
    render_svg(source, tmp, max(256, size * 4))
    image = Image.open(tmp).convert("RGBA")
    tmp.unlink()
    crop = image.crop(image.getbbox())
    target = int(size * 0.82)
    crop.thumbnail((target, target), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), background or (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((size - crop.width) // 2, (size - crop.height) // 2))
    return canvas


# Export fabrication outlines directly from the canonical vectors.
svg_to_dxf(LOGO / "aa-logo.svg", LOGO / "aa-logo-fabrication.dxf")
svg_to_dxf(EMBLEM / "commons-emblem-fabrication.svg", EMBLEM / "commons-emblem-fabrication.dxf")

# AA exports
render_svg(LOGO / "aa-logo.svg", LOGO / "aa-logo-transparent.png", 512)
render_svg(LOGO / "aa-logo.svg", LOGO / "aa-logo-white-background.png", 512, background="#FFFFFF")
render_svg(LOGO / "aa-logo-white.svg", LOGO / "aa-logo-white-transparent.png", 512)

icon_from_aa(96).save(LOGO / "favicon-96x96.png")
icon_from_aa(180, background=(255, 255, 255, 255)).convert("RGB").save(LOGO / "apple-touch-icon.png")
icon_from_aa(192, background=(255, 255, 255, 255)).convert("RGB").save(LOGO / "web-app-manifest-192x192.png")
icon_from_aa(512, background=(255, 255, 255, 255)).convert("RGB").save(LOGO / "web-app-manifest-512x512.png")
icon_from_aa(256).save(LOGO / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

render_svg(LOGO / "technology-commons-lockup.svg", LOGO / "technology-commons-lockup-transparent.png", 1450, 300)
render_svg(LOGO / "technology-commons-lockup.svg", LOGO / "technology-commons-lockup-white-background.png", 1450, 300, background="#FFFFFF")

# Emblem exports
render_svg(EMBLEM / "commons-emblem.svg", EMBLEM / "commons-emblem-transparent.png", 1024)
render_svg(EMBLEM / "commons-emblem.svg", EMBLEM / "commons-emblem-white-background.png", 1024, background="#FFFFFF")

render_svg(EMBLEM / "commons-emblem-monochrome-blue.svg", EMBLEM / "commons-emblem-monochrome-blue-transparent.png", 1024)
render_svg(EMBLEM / "commons-emblem-monochrome-blue.svg", EMBLEM / "commons-emblem-monochrome-blue-white-background.png", 1024, background="#FFFFFF")

render_svg(EMBLEM / "commons-emblem-monochrome-light.svg", EMBLEM / "commons-emblem-monochrome-light-transparent.png", 1024)
render_svg(EMBLEM / "commons-emblem-monochrome-light.svg", EMBLEM / "commons-emblem-monochrome-light-white-background.png", 1024, background="#FFFFFF")
render_svg(EMBLEM / "commons-emblem-monochrome-light.svg", EMBLEM / "commons-emblem-monochrome-light-navy-background.png", 1024, background=NAVY)

# Static social image. This is a single fixed export, not a social-card generator.
seal = Image.open(EMBLEM / "commons-emblem-white-background.png").convert("RGBA")
seal.thumbnail((500, 500), Image.Resampling.LANCZOS)
canvas = Image.new("RGB", (1200, 630), CREAM)
canvas.paste(seal.convert("RGB"), (55, (630 - seal.height) // 2))
draw = ImageDraw.Draw(canvas)
font_path = ROOT.parent / "fonts" / "SourceSans3-VariableFont_wght.ttf"
title_font = ImageFont.truetype(str(font_path), 64)
sub_font = ImageFont.truetype(str(font_path), 30)
draw.text((585, 220), "Technology", fill=NAVY, font=title_font)
draw.text((585, 290), "Commons", fill=NAVY, font=title_font)
draw.text((590, 385), "Learning, making, and growing.", fill="#39415F", font=sub_font)
canvas.save(EMBLEM / "commons-social.png")

print("Technology Commons branding exports generated.")
