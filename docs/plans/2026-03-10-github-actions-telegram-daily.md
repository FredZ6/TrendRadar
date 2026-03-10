# GitHub Actions Telegram Four-Hour Push Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Change the deployed GitHub Actions path so it pushes Telegram digests every four hours starting at 07:00 Winnipeg time using the existing TrendRadar notification stack.

**Architecture:** Reuse the current `python -m trendradar` workflow entrypoint and Telegram sender. Introduce a dedicated scheduler preset for five Winnipeg local-time push windows, then make the workflow opt into that preset through environment variables. Keep periodic wake-ups so DST stays correct.

**Tech Stack:** Python 3.10, `unittest`, YAML config, GitHub Actions

---

### Task 1: Update the scheduler regression test

**Files:**
- Create: `tests/test_daily_morning_digest_schedule.py`
- Modify: `docs/plans/2026-03-10-github-actions-telegram-daily.md`
- Test: `tests/test_daily_morning_digest_schedule.py`

**Step 1: Write the failing test**

```python
class SchedulerPresetTests(unittest.TestCase):
    def test_timeline_declares_every_four_hours_digest_preset(self):
        ...
```

**Step 2: Run test to verify it fails**

Run: `python -m unittest tests.test_daily_morning_digest_schedule -v`
Expected: FAIL because the new preset is not defined yet and the workflow still points to the old one.

**Step 3: Write minimal implementation**

```yaml
every_four_hours_digest:
  periods:
    morning_1:
      start: "07:00"
      end: "09:00"
    midday_1:
      start: "11:00"
      end: "13:00"
    afternoon_1:
      start: "15:00"
      end: "17:00"
    evening_1:
      start: "19:00"
      end: "21:00"
    night_1:
      start: "23:00"
      end: "01:00"
```

**Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_daily_morning_digest_schedule -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_daily_morning_digest_schedule.py config/timeline.yaml
git commit -m "test: cover every four hours schedule"
```

### Task 2: Update the workflow to use the new preset

**Files:**
- Modify: `.github/workflows/crawler.yml`
- Test: `.github/workflows/crawler.yml`

**Step 1: Write the failing expectation**

- Define the behavior in code comments and plan: the workflow must keep the Winnipeg timezone and use the new every-four-hours preset.

**Step 2: Verify current workflow does not meet it**

Run: `rg -n "TIMEZONE|SCHEDULE_PRESET" .github/workflows/crawler.yml`
Expected: finds the old preset value.

**Step 3: Write minimal implementation**

```yaml
env:
  TIMEZONE: America/Winnipeg
  SCHEDULE_PRESET: every_four_hours_digest
```

- Keep periodic scheduling so the app-level scheduler handles DST-safe local timing.

**Step 4: Verify workflow content**

Run: `rg -n "TIMEZONE|SCHEDULE_PRESET" .github/workflows/crawler.yml`
Expected: timezone present; preset changed to `every_four_hours_digest`.

**Step 5: Commit**

```bash
git add .github/workflows/crawler.yml
git commit -m "feat: schedule winnipeg four hour telegram digest"
```

### Task 3: Update docs to match the new cadence

**Files:**
- Modify: `README.md`
- Test: `README.md`

**Step 1: Write the failing expectation**

- Document that Winnipeg delivery now runs every four hours from 07:00 local time and still depends on a real Telegram destination chat id.

**Step 2: Verify current docs miss this Winnipeg-specific guidance**

Run: `rg -n "America/Winnipeg|daily_morning_digest|every_four_hours_digest|TELEGRAM_CHAT_ID" README.md`
Expected: docs still refer to the old daily preset.

**Step 3: Write minimal implementation**

```md
- Workflow uses `America/Winnipeg`
- Workflow uses `every_four_hours_digest`
- Pushes at 07/11/15/19/23 local time
- Rotate leaked bot tokens before enabling Actions
- `TELEGRAM_CHAT_ID` must be the target chat/user/channel ID
```

**Step 4: Verify docs**

Run: `rg -n "America/Winnipeg|every_four_hours_digest|target chat" README.md`
Expected: new guidance is present.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: explain winnipeg four hour telegram deployment"
```

### Task 4: Run focused verification

**Files:**
- Modify: `progress.md`
- Test: `tests/test_daily_morning_digest_schedule.py`

**Step 1: Run targeted tests**

Run: `python3 -m unittest tests.test_daily_morning_digest_schedule -v`
Expected: PASS

**Step 2: Run static content checks**

Run: `rg -n "every_four_hours_digest|America/Winnipeg|07:00|11:00|15:00|19:00|23:00" config/timeline.yaml .github/workflows/crawler.yml README.md`
Expected: new preset/timezone/windows present.

**Step 3: Record evidence**

- Update `progress.md` with actual commands and outcomes.

**Step 4: Commit**

```bash
git add progress.md
git commit -m "chore: record verification for four hour deployment"
```
