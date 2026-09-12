# Technology Commons

A Quarto teaching website for TAS2O, TEJ3M/4M and TTJ3C/4C, shared tools,
resources, a glossary, and Lore. `master` is the canonical branch.

## Build and check

Install Quarto (verified with 1.10.15), Python 3.11+, Node.js, and PyYAML.
No R, Shiny service, worker, or social-card pipeline is required.

```sh
python -m pip install -r requirements.txt
quarto render site
python scripts/check_commons.py --rendered
python -m http.server 6590 --bind 127.0.0.1 --directory site/_site
```

Open http://127.0.0.1:6590. If the Windows Quarto launcher fails under Program
Files, use `C:/Progra~1/Quarto/bin/quarto.cmd render site`.
For editing, use `quarto preview site`. Full renders regenerate the glossary;
page previews reuse its generated presentation.

## Structure

- `site/_quarto.yml`: one navigation, theme, and render configuration.
- `site/tas2`, `site/tej3-4`, `site/ttj3-4`: current course outlines and pages.
- `site/resources`: NICE guide and RevealJS lesson.
- `site/tools`: NICE Project Builder; its CSS/JS live in `site/assets`.
- `site/lore`: current stories and reflections.
- `site/wellbeing`: existing scope page, preserved for the next phase.
- `glossary/glossary.json`: canonical glossary; inherited Backgammon reference
  terms are retained pending technology vocabulary work.
- `site/assets/branding`: canonical AA and corrected lighthouse asset kit.

Historical Backgammon articles in `site/posts` and `site/research` are excluded
from rendering. Older migration and testing notes in `docs` remain historical
references. Use the current [authoring guide](docs/authoring-guide.md),
[branch report](docs/branch-consolidation.md), and
[branding guide](favicons_logos_icons/README.md).

## Attribution and licensing

Adapted from Backgammon Simplified by Marty Gale and contributors. Andrew
Andrade's Commons content and identity are the current site. Preserve inherited
attribution: software is AGPL-3.0-only; educational material is CC BY-SA 4.0.
See [LICENSE.md](LICENSE.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
