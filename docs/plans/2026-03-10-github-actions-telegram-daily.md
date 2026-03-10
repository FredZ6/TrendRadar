# GitHub Actions Telegram Daily Push Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a permanent GitHub Actions deployment path that pushes one Telegram morning digest each Winnipeg day using the existing TrendRadar notification stack.

**Architecture:** Reuse the current `python -m trendradar` workflow entrypoint and Telegram sender. Introduce a dedicated scheduler preset for a once-per-day morning digest, then make the workflow opt into that preset and Winnipeg timezone through environment variables. Remove the repository-specific 7-day auto-disable logic so the automation behaves like a normal personal deployment.

**Tech Stack:** Python 3.10, `unittest`, YAML config, GitHub Actions

---

### Task 1: Add the scheduler regression test

**Files:**
- Create: `tests/test_daily_morning_digest_schedule.py`
- Modify: `docs/plans/2026-03-10-github-actions-telegram-daily.md`
- Test: `tests/test_daily_morning_digest_schedule.py`

**Step 1: Write the failing test**

```python
class SchedulerPresetTests(unittest.TestCase):
    def test_daily_morning_digest_pushes_once_in_morning_window(self):
        ...
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_daily_morning_digest_schedule -v`
Expected: FAIL because the new preset is not defined yet.

**Step 3: Write minimal implementation**

```yaml
daily_morning_digest:
  default:
    collect: true
    analyze: false
    push: false
  periods:
    morning_digest:
      start: "07:00"
      end: "09:00"
      analyze: true
      push: true
      report_mode: "daily"
```

**Step 4: Run test to verify it passes**

Run: `python -m unittest tests.test_daily_morning_digest_schedule -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_daily_morning_digest_schedule.py config/timeline.yaml
git commit -m "test: cover daily morning digest schedule"
```

### Task 2: Update the workflow for permanent Winnipeg delivery

**Files:**
- Modify: `.github/workflows/crawler.yml`
- Test: `.github/workflows/crawler.yml`

**Step 1: Write the failing expectation**

- Define the behavior in code comments and plan: the workflow must no longer auto-disable after 7 days and must opt into Winnipeg daily-morning scheduling.

**Step 2: Verify current workflow does not meet it**

Run: `rg -n "Check Expiration|gh workflow disable|TIMEZONE|SCHEDULE_PRESET" .github/workflows/crawler.yml`
Expected: finds expiration logic and does not find the needed schedule env vars.

**Step 3: Write minimal implementation**

```yaml
env:
  TIMEZONE: America/Winnipeg
  SCHEDULE_PRESET: daily_morning_digest
```

- Remove the expiration/check-in step.
- Keep periodic scheduling so the app-level scheduler handles DST-safe local timing.

**Step 4: Verify workflow content**

Run: `rg -n "Check Expiration|gh workflow disable|TIMEZONE|SCHEDULE_PRESET" .github/workflows/crawler.yml`
Expected: no expiration logic remains; timezone and preset vars are present.

**Step 5: Commit**

```bash
git add .github/workflows/crawler.yml
git commit -m "feat: schedule winnipeg daily telegram digest"
```

### Task 3: Document the operational requirements

**Files:**
- Modify: `README.md`
- Test: `README.md`

**Step 1: Write the failing expectation**

- Document that Winnipeg daily delivery uses GitHub Secrets and that `TELEGRAM_CHAT_ID` must be a real destination chat id, not the bot username.

**Step 2: Verify current docs miss this Winnipeg-specific guidance**

Run: `rg -n "America/Winnipeg|daily_morning_digest|TELEGRAM_CHAT_ID" README.md`
Expected: Telegram secret docs exist, but no Winnipeg preset guidance and no warning about using a real target chat id instead of the bot username.

**Step 3: Write minimal implementation**

```md
- Workflow uses `America/Winnipeg`
- Workflow uses `daily_morning_digest`
- Rotate leaked bot tokens before enabling Actions
- `TELEGRAM_CHAT_ID` must be the target chat/user/channel ID
```

**Step 4: Verify docs**

Run: `rg -n "America/Winnipeg|daily_morning_digest|target chat" README.md`
Expected: new guidance is present.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: explain winnipeg telegram deployment"
```

### Task 4: Run focused verification

**Files:**
- Modify: `progress.md`
- Test: `tests/test_daily_morning_digest_schedule.py`

**Step 1: Run targeted tests**

Run: `python -m unittest tests.test_daily_morning_digest_schedule -v`
Expected: PASS

**Step 2: Run static content checks**

Run: `rg -n "daily_morning_digest|America/Winnipeg|gh workflow disable" config/timeline.yaml .github/workflows/crawler.yml README.md`
Expected: preset/timezone present, disable logic absent.

**Step 3: Record evidence**

- Update `progress.md` with actual commands and outcomes.

**Step 4: Commit**

```bash
git add progress.md
git commit -m "chore: record verification for telegram daily deployment"
```
