# GitHub Actions Telegram Four-Hour Push Design

## Summary

Deploy TrendRadar on GitHub Actions so it delivers Telegram pushes every four hours starting at `07:00` in `America/Winnipeg`, while remaining stable across daylight saving time changes.

## Context

- The repository already contains a scheduled GitHub Actions workflow at [`.github/workflows/crawler.yml`](/Users/fredz/Downloads/trend Radar/.github/workflows/crawler.yml).
- Telegram delivery is already implemented in [`trendradar/notification/dispatcher.py`](/Users/fredz/Downloads/trend Radar/trendradar/notification/dispatcher.py) and [`trendradar/notification/senders.py`](/Users/fredz/Downloads/trend Radar/trendradar/notification/senders.py).
- Runtime config already supports `TIMEZONE`, `SCHEDULE_PRESET`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` environment overrides in [`trendradar/core/loader.py`](/Users/fredz/Downloads/trend Radar/trendradar/core/loader.py).

## Options Considered

### Option 1: Single daily GitHub cron

- Set one UTC cron and let the workflow run once per day.
- Reject: GitHub cron is UTC-only, so Winnipeg’s DST shift would move the local delivery time away from `07:00`.

### Option 2: Seasonal crons

- Maintain separate winter/summer UTC crons.
- Reject: operationally brittle and unnecessary because the app already has a timezone-aware scheduler.

### Option 3: Periodic wake-up plus app-level local-time windows

- Keep GitHub Actions waking the app periodically.
- Add a dedicated schedule preset that pushes once in each Winnipeg local-time window.
- Remove the repository’s 7-day trial auto-disable behavior for permanent personal use.
- Chosen: this is the only approach that stays correct through DST without manual cron maintenance.

## Approved Design

### Architecture

- Add a new scheduler preset in [`config/timeline.yaml`](/Users/fredz/Downloads/trend Radar/config/timeline.yaml) for every-four-hours delivery.
- The preset will:
  - always collect data,
  - stay quiet outside the configured push windows,
  - analyze and push once during each active window,
  - use `daily` report mode so every push summarizes all collected items for that local day so far.
- The GitHub Actions workflow will:
  - keep periodic wake-ups,
  - inject `TIMEZONE=America/Winnipeg`,
  - inject `SCHEDULE_PRESET=every_four_hours_digest`.

### Time Behavior

- The push windows will span two hours each, not a single minute.
- Reason: GitHub Actions scheduled runs can drift, and the repository’s own timeline docs already recommend wider windows for reliability.
- `once.push: true` ensures only the first run inside each window pushes.
- The user-approved Winnipeg local schedule is:
  - `07:00-09:00`
  - `11:00-13:00`
  - `15:00-17:00`
  - `19:00-21:00`
  - `23:00-01:00`

### Telegram Behavior

- Delivery will continue through the existing Telegram dispatcher.
- No new Telegram sender code is required.
- Deployment still depends on valid GitHub Secrets:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`

### Error Handling

- If Telegram secrets are missing or invalid, the existing dispatcher path will skip/fail the channel and log the issue.
- The code change will not attempt to store secrets in tracked files.
- Because a token was pasted into chat, the user must rotate it before enabling the workflow.

### Testing

- Add a regression test around the new preset:
  - workflow points at the new preset,
  - timeline defines the five local-time windows,
  - old trial-expiration logic remains absent.
- Verify the targeted test run locally.

## Expected Outcome

- GitHub Actions runs continuously enough to survive DST and scheduler drift.
- TrendRadar sends at most one Telegram digest in each of the five approved Winnipeg time windows.
