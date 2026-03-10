# GitHub Actions Telegram Daily Push Design

## Summary

Deploy TrendRadar on GitHub Actions so it delivers one Telegram push each day at approximately `07:00` in `America/Winnipeg`, while remaining stable across daylight saving time changes.

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

### Option 3: Periodic wake-up plus app-level morning window

- Keep GitHub Actions waking the app periodically.
- Add a dedicated schedule preset that only pushes once inside a Winnipeg morning window.
- Remove the repository’s 7-day trial auto-disable behavior for permanent personal use.
- Chosen: this is the only approach that stays correct through DST without manual cron maintenance.

## Approved Design

### Architecture

- Add a new scheduler preset in [`config/timeline.yaml`](/Users/fredz/Downloads/trend Radar/config/timeline.yaml) for a once-per-day morning digest.
- The preset will:
  - always collect data,
  - stay quiet outside the morning window,
  - analyze and push once during the morning window,
  - use `daily` report mode so the morning push summarizes all collected items for that local day so far.
- The GitHub Actions workflow will:
  - keep periodic wake-ups,
  - inject `TIMEZONE=America/Winnipeg`,
  - inject `SCHEDULE_PRESET=daily_morning_digest`,
  - remove the 7-day auto-disable/check-in logic.

### Time Behavior

- The morning push window will span two hours, not a single minute.
- Reason: GitHub Actions scheduled runs can drift, and the repository’s own timeline docs already recommend wider windows for reliability.
- `once.push: true` ensures only the first run inside that window pushes that day.

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

- Add a regression test around the scheduler preset:
  - inside the morning window: push enabled, once enabled, daily mode,
  - outside the window: push disabled.
- Verify the targeted test run locally.

## Expected Outcome

- GitHub Actions runs continuously enough to survive DST and scheduler drift.
- TrendRadar sends at most one Telegram morning digest per Winnipeg day.
- The repo no longer disables itself after 7 days.
