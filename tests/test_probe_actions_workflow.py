import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "probe-actions.yml"


class ProbeActionsWorkflowTests(unittest.TestCase):
    def test_probe_workflow_exists_and_is_minimal(self) -> None:
        self.assertTrue(PROBE_WORKFLOW_PATH.exists(), "probe workflow file should exist")

        content = PROBE_WORKFLOW_PATH.read_text(encoding="utf-8")

        self.assertIn("name: Actions Probe", content)
        self.assertIn("workflow_dispatch:", content)
        self.assertIn("runs-on: ubuntu-latest", content)
        self.assertIn('echo "probe-ok"', content)


if __name__ == "__main__":
    unittest.main()
