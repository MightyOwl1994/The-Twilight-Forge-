# Project State

_Last updated: 2026-04-07_

## What this project is
The Twilight Forge (package name: `rp-foundry`) is a small, reusable Python CLI for generating roleplay scene context packets.

This is an early foundation version. The focus is reliability, readability, and clear file-based workflows.

## Current capabilities
- Campaign folder structure under `campaigns/<campaign_name>/`
- Scene packet generation from required files + selected optional context
- Scene logging
- Draft update artifact generation (suggestions only, no auto-write to canon files)
- Campaign status/health check command

## Design direction (important)
- Keep the system setting-agnostic
- Do not hard-wire to Twilight lore
- Prefer simple, sharp systems over complex architecture
- Keep humans in control of canon updates

## Known limits right now
- Selection logic is intentionally basic (keyword overlap)
- CLI-first workflow (no web UI)
- No automated canon/state mutation

## Update this file when
- A major capability is added/removed
- Project direction changes
- The “current version” or scope changes
