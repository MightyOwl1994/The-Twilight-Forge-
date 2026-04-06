# rp-foundry

`rp-foundry` is a small, setting-agnostic Python CLI for building curated roleplay scene packets.
It is intentionally simple and file-based so humans stay in control of review and canon updates.

## Version 1 goals

- Keep the engine readable, deterministic, and easy to extend.
- Load campaign inputs from `campaigns/<campaign_name>/`.
- Build scene packets from required files plus selected optional context.
- Log scene outputs.
- Draft suggested canon/state update notes (without auto-applying changes).
- Report campaign health via a status command.

## Requirements

- Python 3.11+

## Installation

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Campaign layout

Each campaign uses this structure:

```text
campaigns/
  <campaign_name>/
    config.yaml
    inputs/
      current_state.txt        # required
      style_bible.txt          # required
      campaign_bible.txt       # required
      lore_appendix.txt        # optional
      roster_threads.txt       # optional
      open_threads.txt         # optional
      recent_summary.txt       # optional
      player_input.txt         # optional convenience input file
    outputs/
    logs/
```

## CLI usage

### 1) Build a packet

You can provide player input in **either** of two ways:

- Inline text with `--player-input`
- A text file with `--player-input-file`

`build-packet` requires **exactly one** of those options.

```bash
rp-foundry build-packet \
  --campaign example_campaign \
  --player-input-file campaigns/example_campaign/inputs/player_input.txt
```

Inline text example:

```bash
rp-foundry build-packet \
  --campaign example_campaign \
  --player-input "I want to find the courier and decide whether to relight the summit beacon."
```

Behavior:
- Always includes `current_state.txt`, `style_bible.txt`, and `campaign_bible.txt`.
- Uses deterministic keyword overlap against player input to select optional chunks.
- Writes `campaigns/<campaign>/outputs/packet-<label or timestamp>.txt`.
- If neither input option is provided, the CLI shows a clear error.
- If both are provided together, the CLI shows a clear conflict error.
- If a file path is wrong, the CLI shows a beginner-friendly `Error: ...` message (no Python traceback).
- If the file exists but is empty, the CLI asks you to add content or use `--player-input`.

### 2) Log a scene

```bash
rp-foundry log-scene \
  --campaign example_campaign \
  --scene-file path/to/scene_output.txt \
  --source-packet packet-20260101-120000.txt
```

Alternative:

```bash
rp-foundry log-scene --campaign example_campaign --scene-text "Short scene transcript..."
```

### 3) Draft a suggested update

```bash
rp-foundry draft-update \
  --campaign example_campaign \
  --scene-file path/to/scene_output.txt
```

This creates a review artifact in `outputs/` and does **not** modify canon files automatically.

### 4) Campaign status

```bash
rp-foundry status --campaign example_campaign
```

Shows missing required files, optional availability, and output/log counts.

## Selection logic (V1)

Selection is intentionally simple:

1. Split optional source files into sections (heading and blank-line chunking).
2. Extract keyword tokens from player input.
3. Score each section by overlap count.
4. Select top sections (default max 3) by score, then original order for tie-breaks.

No machine learning, no background simulation, no autonomous changes.

## Tests

Run:

```bash
pytest
```

Current tests cover:
- Deterministic keyword section selection.
- Packet building with required + matching optional content.
- Missing required input error behavior.

## Extensibility notes

Planned extension points are lightweight and safe:
- Add new optional input files by updating constants in `io_utils.py`.
- Swap or expand selection logic in `selection.py`.
- Add additional artifact builders in `engine.py`.
- Extend CLI commands in `cli.py`.

The default architecture is intentionally conservative so workflows remain transparent and reviewer-driven.
