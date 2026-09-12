from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    """Run one required build step from the repository root."""
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def main() -> int:
    # Full project renders generate and validate the glossary. Incremental page
    # previews reuse the committed generated glossary files so editing a lesson
    # or Lore post does not launch the glossary pipeline on every refresh.
    if os.getenv("QUARTO_PROJECT_RENDER_ALL") != "1":
        print("Incremental preview: reusing generated Commons glossary files.")
        print(
            "After glossary edits, run: python scripts/commons_glossary.py generate"
        )
        return 0

    print("Full project render: generating Commons glossary source.")
    run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "commons_glossary.py"),
            "generate",
        ]
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
