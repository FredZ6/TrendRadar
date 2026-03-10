import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TIMELINE_PATH = ROOT / "config" / "timeline.yaml"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "crawler.yml"


class EveryFourHoursDigestConfigTests(unittest.TestCase):
    def test_timeline_declares_every_four_hours_digest_preset(self) -> None:
        content = TIMELINE_PATH.read_text(encoding="utf-8")

        self.assertIn("every_four_hours_digest:", content)
        self.assertIn('start: "07:00"', content)
        self.assertIn('end: "09:00"', content)
        self.assertIn('start: "11:00"', content)
        self.assertIn('end: "13:00"', content)
        self.assertIn('start: "15:00"', content)
        self.assertIn('end: "17:00"', content)
        self.assertIn('start: "19:00"', content)
        self.assertIn('end: "21:00"', content)
        self.assertIn('start: "23:00"', content)
        self.assertIn('end: "01:00"', content)
        self.assertIn('report_mode: "daily"', content)
        self.assertIn('ai_mode: "daily"', content)

    def test_workflow_uses_winnipeg_preset_without_trial_disable(self) -> None:
        content = WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("TIMEZONE: America/Winnipeg", content)
        self.assertIn("SCHEDULE_PRESET: every_four_hours_digest", content)
        self.assertNotIn("Check Expiration", content)
        self.assertNotIn("gh workflow disable", content)


if __name__ == "__main__":
    unittest.main()
