# Changelog

Simple session-level history. Keep entries short.

## 2026-04-07
- Added a focused `status` CLI edge-case test batch for missing `--campaign` usage and a missing `inputs/` folder, including clear required-file reporting and no traceback for expected user mistakes.

## 2026-04-07
- Added a small non-`build-packet` CLI edge-case test batch for `log-scene` and `draft-update` (missing scene input, invalid scene file paths, empty scene-file behavior, and clean no-traceback user errors).

## 2026-04-07
- Added a small batch of CLI edge-case tests covering player-input argument mistakes, missing/empty player input files, and missing required campaign input files with clean (non-traceback) user-facing errors.

## 2026-04-07
- Added a second small sample campaign at `campaigns/frontier_watch/` (required files + config) to demonstrate setting portability beyond the original example.

## 2026-04-07
- Improved `README.md` beginner onboarding with a literal Windows first-run walkthrough (clone, venv setup, install, first command order, expected files, troubleshooting).

## 2026-04-07
- Added a lightweight documentation system in `docs/`:
  - `PROJECT_STATE.md`
  - `DECISIONS.md`
  - `CHANGELOG.md`
  - `NEXT_STEPS.md`
- Updated `README.md` with a new "Project Documentation" section.

## Earlier baseline (pre-docs)
- Early CLI foundation in place
- Supports campaign folders, packet generation, scene logging, and draft update artifacts

## Update this file when
- A session ends and something meaningful changed
- You want a quick “what happened recently?” record
