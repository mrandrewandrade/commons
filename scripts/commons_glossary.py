#!/usr/bin/env python3
"""Generate and validate the Technology Commons glossary source."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:
    from scripts import learn_glossary
except ImportError:  # Direct execution sets sys.path to scripts/.
    import learn_glossary  # type: ignore[no-redef]


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DATA_PATH = REPOSITORY_ROOT / "site" / "data" / "glossary.json"
GENERATED_ENTRIES_PATH = REPOSITORY_ROOT / "site" / "glossary" / "_entries.html"
GENERATED_LOOKUP_PATH = REPOSITORY_ROOT / "site" / "assets" / "bs-glossary-lookup.json"


def run_source(command: str) -> None:
    subprocess.run(
        [
            sys.executable,
            str(REPOSITORY_ROOT / "scripts" / "glossary_source.py"),
            command,
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
    )


def validate_current_presentation() -> dict[str, int]:
    data = learn_glossary.read_json(PUBLIC_DATA_PATH)
    entries = learn_glossary.validate_public_data(data)
    expected = {
        GENERATED_ENTRIES_PATH: learn_glossary.build_entries_html(entries, {}, {}),
        GENERATED_LOOKUP_PATH: learn_glossary.build_lookup_data(entries, {}),
    }
    for path, content in expected.items():
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            raise learn_glossary.ValidationError(
                f"Stale glossary presentation: {path.name}; "
                "run python scripts/commons_glossary.py generate"
            )
    learn_glossary.assert_no_forbidden_text(
        PUBLIC_DATA_PATH.read_text(encoding="utf-8"),
        "tracked public glossary data",
    )

    required = (GENERATED_ENTRIES_PATH, GENERATED_LOOKUP_PATH)
    missing = [path for path in required if not path.is_file()]
    if missing:
        raise learn_glossary.ValidationError(
            "Missing glossary presentation files: "
            + ", ".join(
                str(path.relative_to(REPOSITORY_ROOT)) for path in missing
            )
        )

    lookup = learn_glossary.read_json(GENERATED_LOOKUP_PATH)
    lookup_entries = lookup.get("entries") if isinstance(lookup, dict) else None
    if not isinstance(lookup_entries, list) or len(lookup_entries) != len(entries):
        raise learn_glossary.ValidationError(
            "Glossary lookup data does not match the canonical term count"
        )

    return {
        "canonical_entries": len(entries),
        "lookup_entries": len(lookup_entries),
    }


def generate() -> dict[str, int]:
    run_source("generate-source")
    entries = learn_glossary.validate_public_data(
        learn_glossary.read_json(PUBLIC_DATA_PATH)
    )
    # The inherited lesson corpus was retired. Preserve definitions without
    # carrying forward relationships to pages that no longer exist.
    learn_glossary.write_if_changed(
        GENERATED_ENTRIES_PATH, learn_glossary.build_entries_html(entries, {}, {})
    )
    learn_glossary.write_if_changed(
        GENERATED_LOOKUP_PATH, learn_glossary.build_lookup_data(entries, {})
    )
    return validate_current_presentation()


def validate() -> dict[str, int]:
    run_source("check-source")
    return validate_current_presentation()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        nargs="?",
        default="generate",
        choices=("generate", "validate"),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = generate() if args.command == "generate" else validate()
    except (
        OSError,
        subprocess.CalledProcessError,
        learn_glossary.ValidationError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Technology Commons glossary check passed: "
        + ", ".join(f"{key}={value}" for key, value in sorted(result.items()))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
