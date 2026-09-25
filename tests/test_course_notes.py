from __future__ import annotations

import copy
import json
import unittest

from scripts import course_notes


class CourseNotesManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = course_notes.load_source()
        cls.manifest = course_notes.build_manifest(cls.source)
        cls.lessons = cls.manifest["lessons"]

    def test_active_course_sequences_are_exact(self) -> None:
        routes_by_course: dict[str, list[str]] = {}
        for lesson in self.lessons:
            routes_by_course.setdefault(lesson["course_id"], []).append(lesson["route"])
        self.assertEqual(
            routes_by_course["tas"],
            [
                "/commons/tas2/01-nice-design-process/01-needs-necessities.html",
                "/tech-edu-resources/tas2/01-nice-design-process/02-investigate-inquire.html",
            ],
        )
        self.assertEqual(
            routes_by_course["tej"],
            [
                "/tech-edu-resources/tej3-4/01-number-systems/01-significant-figures.html",
                "/tech-edu-resources/tej3-4/01-number-systems/02-powers-of-10.html",
                "/tech-edu-resources/tej3-4/01-number-systems/06-scientific-calculator.html",
                "/tech-edu-resources/tej3-4/01-number-systems/03-scientific-notation.html",
                "/tech-edu-resources/tej3-4/01-number-systems/04-engineering-notation.html",
                "/tech-edu-resources/tej3-4/01-number-systems/05-metric-prefixes.html",
            ],
        )

    def test_course_boundaries_stop_cleanly(self) -> None:
        for course_id in ("tas", "tej"):
            course_lessons = [
                lesson for lesson in self.lessons if lesson["course_id"] == course_id
            ]
            self.assertIsNone(course_lessons[0]["previous_route"])
            self.assertIsNone(course_lessons[-1]["next_route"])
        all_routes = {lesson["route"] for lesson in self.lessons}
        self.assertFalse(any("identity-listening" in route for route in all_routes))
        self.assertFalse(any(route.endswith("/index.html") for route in all_routes))

    def test_cross_course_link_fails_validation(self) -> None:
        broken = copy.deepcopy(self.manifest)
        tas_lessons = [
            lesson for lesson in broken["lessons"] if lesson["course_id"] == "tas"
        ]
        tej_first = next(
            lesson for lesson in broken["lessons"] if lesson["course_id"] == "tej"
        )
        tas_lessons[-1]["next_route"] = tej_first["route"]
        with self.assertRaisesRegex(course_notes.ValidationError, "broken next route"):
            course_notes.validate_manifest(broken)

    def test_generated_manifest_is_current(self) -> None:
        tracked = json.loads(course_notes.OUTPUT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(tracked, self.manifest)


if __name__ == "__main__":
    unittest.main()
