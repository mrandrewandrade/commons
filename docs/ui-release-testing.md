# UI release testing

Use this procedure before a site release when UI changes need a full validation pass.

## Build the site

Render the project first. The generated site is written to `site/_site`.

```sh
python -m pip install -r requirements.txt
quarto render site
python scripts/check_commons.py --rendered
```

## Release checks

Run the compatibility entrypoint:

```sh
bash scripts/release-ui-check.sh
```

The release runner combines source, unit, static rendered-site, and JavaScript checks. The browser layer is implemented by `scripts/release_ui_browser_check.mjs`, and the representative page and viewport set is defined in `scripts/ui_release_manifest.json`.

Allow up to **90 minutes** for the complete release procedure when browser checks, screenshots, and review are included.

If any layer fails, fix the source and rebuild `site/_site` before re-running the checks.
