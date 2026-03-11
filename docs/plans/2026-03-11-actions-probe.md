# GitHub Actions Queue Probe Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a minimal probe workflow that can prove whether GitHub Actions in this repository can schedule any job at all.

**Architecture:** Keep the probe isolated from the main crawler workflow. Use TDD with a file-content regression test, then add one minimal manual workflow and trigger it after pushing.

**Tech Stack:** GitHub Actions YAML, Python 3.11 `unittest`, GitHub CLI

---

### Task 1: Add the failing probe workflow regression test

**Files:**
- Create: `tests/test_probe_actions_workflow.py`
- Test: `tests/test_probe_actions_workflow.py`

**Step 1: Write the failing test**

```python
def test_probe_workflow_exists_and_is_minimal(self):
    ...
```

**Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_probe_actions_workflow -v`
Expected: FAIL because `.github/workflows/probe-actions.yml` does not exist yet.

**Step 3: Write minimal implementation**

```yaml
name: Actions Probe
on:
  workflow_dispatch:
jobs:
  probe:
    runs-on: ubuntu-latest
    steps:
      - run: echo "probe-ok"
```

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_probe_actions_workflow -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_probe_actions_workflow.py .github/workflows/probe-actions.yml
git commit -m "test: add actions probe workflow coverage"
```

### Task 2: Push and trigger the probe

**Files:**
- Modify: `.github/workflows/probe-actions.yml`

**Step 1: Verify working tree**

Run: `git status --short`
Expected: only intended files staged or tracked.

**Step 2: Push**

Run: `git push origin master`
Expected: remote `master` updated.

**Step 3: Trigger the probe**

Run: `gh workflow run probe-actions.yml -R FredZ6/TrendRadar --ref master`
Expected: new run URL returned.

**Step 4: Inspect run metadata**

Run: `gh api repos/FredZ6/TrendRadar/actions/runs/<id>/jobs`
Expected: either at least one job is created, or `0` jobs confirms the queue-layer failure.

**Step 5: Commit follow-up only if needed**

```bash
git commit -m "docs: record actions probe results"
```
