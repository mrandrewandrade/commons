from __future__ import annotations

import copy
import inspect
import json
import unittest

from scripts import glossary_source as source
from scripts import learn_glossary


class CanonicalGlossaryJsonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = source.load_contract_json()
        cls.serialized, cls.report = source.build_production_source()
        cls.data = json.loads(cls.serialized)

    def test_canonical_json_is_the_only_production_input(self) -> None:
        self.assertEqual(
            source.GLOSSARY_SOURCE_PATH,
            learn_glossary.REPOSITORY_ROOT / "glossary" / "glossary.json",
        )
        implementation = inspect.getsource(source.build_production_source)
        self.assertIn("load_contract_json", implementation)
        self.assertNotIn("parse_markdown", implementation)
        self.assertNotIn("glossary_old", implementation)
        self.assertNotIn("staged", implementation)

    def test_only_published_entries_are_projected(self) -> None:
        self.assertEqual(len(self.entries), 16)
        self.assertEqual(self.report["canonical_entries"], 16)
        self.assertEqual(self.report["published_entries"], 16)
        self.assertEqual(self.report["aliases"], 21)
        self.assertEqual(len(self.data["entries"]), 16)
        self.assertEqual(
            {entry["slug"] for entry in self.data["entries"]},
            set(self.entries),
        )

    def test_contract_fields_map_without_rewriting_authoritative_json(self) -> None:
        source_entry = self.entries["nice-design-process"]
        generated = {
            entry["slug"]: entry for entry in self.data["entries"]
        }["nice-design-process"]
        self.assertEqual(generated["term"], source_entry["term"])
        self.assertEqual(generated["short_definition"], source_entry["short_definition"])
        self.assertEqual(generated["definition"], source_entry["long_definition"])
        self.assertEqual(generated["categories"], source_entry["categories"])
        self.assertEqual(generated["learning_tracks"], source_entry["tracks"])
        self.assertEqual(generated["date_added"], source_entry["added"])

    def test_related_terms_resolve_to_published_canonicals(self) -> None:
        published = set(self.entries)
        for slug, entry in self.entries.items():
            self.assertLessEqual(set(entry["related_terms"]), published, slug)
        self.assertEqual(self.report["unresolved_related_terms"], 0)

    def test_basic_unit_aliases_are_preserved(self) -> None:
        self.assertIn("amps", self.entries["ampere"]["aliases"])
        self.assertIn("volts", self.entries["volt"]["aliases"])
        self.assertIn("m/s", self.entries["metres-per-second"]["aliases"])
        self.assertIn("m/s²", self.entries["metres-per-second-squared"]["aliases"])
        self.assertIn("N.I.C.E.", self.entries["nice-design-process"]["aliases"])

    def test_duplicate_raw_json_keys_fail_before_normal_parsing(self) -> None:
        with self.assertRaisesRegex(source.ValidationError, "Duplicate raw JSON key"):
            json.loads(
                '{"one":{"term":"One"},"one":{"term":"Other"}}',
                object_pairs_hook=source._reject_duplicate_keys,
            )

    def test_alias_collision_and_broken_inline_target_fail(self) -> None:
        collision = copy.deepcopy(self.entries)
        collision["ampere"]["aliases"] = ["Voltage"]
        with self.assertRaisesRegex(source.ValidationError, "conflicts with a canonical"):
            source.validate_contract_entries(collision)

        broken = copy.deepcopy(self.entries)
        broken["nice-design-process"]["inline_terms"] = {
            "design cycle": "not-published"
        }
        with self.assertRaisesRegex(source.ValidationError, "broken inline target"):
            source.validate_contract_entries(broken)

    def test_generation_is_deterministic_and_tracked_output_is_current(self) -> None:
        first, _ = source.build_production_source()
        second, _ = source.build_production_source()
        self.assertEqual(first, second)
        self.assertEqual(
            learn_glossary.PUBLIC_DATA_PATH.read_text(encoding="utf-8"),
            first,
        )


if __name__ == "__main__":
    unittest.main()
