# Commons verification

```sh
python scripts/check_commons.py
quarto render site
python scripts/check_commons.py --rendered
```

Checks cover glossary freshness, all retained Python/JavaScript tests, JavaScript
syntax, and rendered local links/fragments, images, scripts, and CSS URLs.
`python scripts/check_commons_browser.py` adds Chromium checks after installing
Playwright and Chromium. Screenshots go to ignored `.tools/review`.

Older quality-analysis helpers remain reusable test utilities. Their historical
Backgammon route manifests and SOPs are not Commons release criteria. Tests for
removed publication/services/engine code and the deleted corpus were retired;
their history remains in Git.
