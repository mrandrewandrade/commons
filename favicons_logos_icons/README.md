# Technology Commons brand assets

The single served kit is in `site/assets/branding/`.

- `logo/aa-logo.svg`: canonical black AA mark for small sizes and favicons.
- `logo/aa-logo-white.svg`: reversed AA mark.
- `logo/technology-commons-lockup.svg`: existing outlined wordmark and AA lockup.
- `emblem/commons-emblem.svg`: corrected lighthouse and beam gradients from the
  design branch, with navy and light monochrome variants alongside it.
- `emblem/commons-emblem-fabrication.svg`: fabrication master. DXF outlines are
  generated from it; the AA DXF is generated directly from `aa-logo.svg`.

PNG, ICO, and DXF exports are committed so the site needs no graphics dependencies.
Use AA below roughly 130 pixels and the detailed emblem at larger sizes.
The corrected emblem uses navy #062650, gold #D49A00, and off-white #FAF7F2.
The existing personal lockup retains its original colours. Historical source
images stay with the Lore story.

Regenerate only when vector masters change:

```sh
python -m pip install cairosvg pillow ezdxf svgpathtools
python favicons_logos_icons/generate_brand_assets.py
```

CairoSVG needs system Cairo. The manual GitHub workflow produces downloadable
exports on Linux. Review regenerated files before committing. No compatibility
aliases or copied root favicons are maintained. `commons-social.png` is one
static share graphic. Check fabrication dimensions and contours in CAD before use.
