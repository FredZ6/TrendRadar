# GitHub Actions Queue Probe Design

## Summary

Add a minimal GitHub Actions workflow dedicated to diagnosing whether this repository can schedule any GitHub-hosted jobs at all.

## Context

- Multiple `Get Hot News` runs are stuck in `queued`.
- GitHub accepts the workflow dispatch, but creates `0` jobs for each run.
- Repository Actions permissions are enabled and the workflow state is `active`.
- This strongly suggests a queueing / runner-assignment issue rather than a TrendRadar application problem.

## Options Considered

### Option 1: Keep retrying the main crawler workflow

- Reject: the crawler workflow is too large and has too many moving parts. It is a poor probe for a platform-level queue issue.

### Option 2: Replace the crawler workflow with a minimal test job

- Reject: destructive to the deployed workflow and unnecessary.

### Option 3: Add a separate probe workflow

- Chosen.
- The workflow will:
  - be manually triggerable only,
  - run on `ubuntu-latest`,
  - contain one shell step that prints a fixed line.
- If this probe also remains `queued` with no jobs created, the problem is at the repository / GitHub Actions scheduling layer.

## Approved Design

### Architecture

- Add [probe-actions.yml](/Users/fredz/Downloads/trend Radar/.github/workflows/probe-actions.yml).
- Keep it independent from existing TrendRadar workflows.
- Add a small regression test to assert the probe file exists and stays minimal.

### Behavior

- Trigger path: `workflow_dispatch`
- Runner: `ubuntu-latest`
- Job body: one job, one step, `echo "probe-ok"`

### Verification

- Run a failing content test first.
- Add the workflow.
- Re-run the content test.
- Push to `master`.
- Manually trigger the probe workflow and inspect whether GitHub creates a job.

## Expected Outcome

- We either prove the repository can run a trivial workflow, or we isolate the issue as a GitHub Actions scheduling problem outside the app code.
