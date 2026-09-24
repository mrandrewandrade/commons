# Technological Education Resources

A Quarto teaching website for TAS2O, TEJ3M/4M and TTJ3C/4C, with shared tools, resources, a glossary, Lore, and well-being material.

## Build and check

Install Quarto, Python 3.11+, Node.js, and the Python requirements.

```sh
python -m pip install -r requirements.txt
quarto render site
python scripts/check_commons.py --rendered
```

For editing, use:

```sh
quarto preview site
```

The rendered output is `site/_site`. Do not edit generated output directly.

## Main structure

- `site/_quarto.yml`: navigation, theme, and render configuration.
- `site/tas2`, `site/tej3-4`, `site/ttj3-4`: course pages.
- `site/resources`: classroom resources and NICE design-process material.
- `site/tools`: student-facing tools, including the NICE Project Builder.
- `site/lore`: stories, reflections, and design-process examples.
- `site/wellbeing`: classroom well-being material.
- `site/assets`: site styling, scripts, images, icons, and branding.
- `glossary/glossary.json`: glossary source.
- `docs/authoring-guide.md`: editing and build notes.
- `docs/website-colour-accessibility-contract.md`: colour and contrast requirements.
- `favicons_logos_icons`: source files and generator for brand assets.

Temporary build output, local tool output, logs, caches, and virtual environments are excluded by `.gitignore`.

## Attribution and licensing

Technology Commons was adapted from earlier Backgammon Simplified source material. Required inherited attribution and third-party notices are retained. Original project code and executable materials use AGPL-3.0-only, while original educational content uses CC BY-SA 4.0. See `LICENSE.md`, `LICENSES/`, `THIRD_PARTY_NOTICES.md`, and `site/licensing.qmd`.
