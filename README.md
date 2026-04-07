# The Twilight Forge (`rp-foundry`)

`rp-foundry` is a small, setting-agnostic Python CLI for building curated roleplay scene packets.
It is intentionally simple and file-based so humans stay in control of review and canon updates.

## First-run walkthrough (Windows, beginner-friendly)

This is a literal first run you can copy step-by-step in **Windows PowerShell**.

### 0) What you should have first

- Python 3.11+ installed.
- Git installed.
- A PowerShell window open.

### 1) Clone the repo

```powershell
git clone https://github.com/<your-org-or-user>/The-Twilight-Forge-.git
```

### 2) Open the repo folder in a terminal

```powershell
cd .\The-Twilight-Forge-
```

If you are not sure where you are, run:

```powershell
pwd
```

### 3) Create a virtual environment (Windows)

```powershell
py -3.11 -m venv .venv
```

If `py` does not work on your machine, try:

```powershell
python -m venv .venv
```

### 4) Activate the virtual environment in PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, your prompt usually shows `(.venv)` on the left.

### 5) Install the project

```powershell
python -m pip install -e .[dev]
```

### 6) Prepare your first input file

Open this file and add at least one line of player intent text:

- `campaigns/example_campaign/inputs/player_input.txt`

Example content:

```text
I want to find the courier and decide whether to relight the summit beacon.
```

### 7) Run the CLI commands in this exact order (first test)

1. Check campaign status first:

```powershell
rp-foundry status --campaign example_campaign
```

2. Build your first packet (using a fixed label so the output filename is predictable):

```powershell
rp-foundry build-packet --campaign example_campaign --player-input-file campaigns/example_campaign/inputs/player_input.txt --label firsttest
```

3. Log a scene (replace the scene file path with your own text file):

```powershell
rp-foundry log-scene --campaign example_campaign --scene-file path\\to\\scene_output.txt --source-packet packet-firsttest.txt
```

4. Draft a suggested update from that scene:

```powershell
rp-foundry draft-update --campaign example_campaign --scene-file path\\to\\scene_output.txt
```

5. Run status again to confirm outputs/logs changed:

```powershell
rp-foundry status --campaign example_campaign
```

### 8) What files/folders to expect

Before running commands (typical):

```text
campaigns/
  example_campaign/
    config.yaml
    inputs/
      current_state.txt
      style_bible.txt
      campaign_bible.txt
      lore_appendix.txt (optional)
      roster_threads.txt (optional)
      open_threads.txt (optional)
      recent_summary.txt (optional)
      player_input.txt (optional convenience input file)
    outputs/
    logs/
```

After running the first test above:

```text
campaigns/
  example_campaign/
    outputs/
      packet-firsttest.txt
      draft-update-*.txt
    logs/
      scene-log-*.txt
```

(Exact timestamped filenames vary.)

### 9) Troubleshooting (common beginner mistakes)

- **"command not found"**
  - If `rp-foundry` is not recognized, your virtual environment is usually not active, or install did not finish.
  - Re-run:
    - `.\\.venv\\Scripts\\Activate.ps1`
    - `python -m pip install -e .[dev]`

- **venv not activated**
  - If you do not see `(.venv)` in the prompt, run:
    - `.\\.venv\\Scripts\\Activate.ps1`

- **wrong file path**
  - Keep paths relative to repo root.
  - Example correct player input path:
    - `campaigns/example_campaign/inputs/player_input.txt`

- **empty player input file**
  - `build-packet` needs real text in the file.
  - Add at least one non-empty line to `player_input.txt`, or use `--player-input "..."`.

## Version 1 goals

- Keep the engine readable, deterministic, and easy to extend.
- Load campaign inputs from `campaigns/<campaign_name>/`.
- Build scene packets from required files plus selected optional context.
- Log scene outputs.
- Draft suggested canon/state update notes (without auto-applying changes).
- Report campaign health via a status command.

## Project Documentation

To keep context easy to recover between sessions, this repo uses a small docs set in `docs/`:

- `docs/PROJECT_STATE.md` — Quick snapshot of where the project is right now (scope, capabilities, limits, direction).
- `docs/DECISIONS.md` — Short decision log (what we decided, why, and tradeoffs).
- `docs/CHANGELOG.md` — Session-level “what changed” history.
- `docs/NEXT_STEPS.md` — Active short to-do list and immediate priorities.

When to update each doc:
- Update **PROJECT_STATE** when the project’s current scope or direction changes.
- Update **DECISIONS** when you make (or reject) an important technical/product choice.
- Update **CHANGELOG** at the end of any work session with meaningful changes.
- Update **NEXT_STEPS** whenever priorities shift or tasks are completed.

Keep these docs practical and lightweight—this is not meant to become a big wiki.

## Requirements

- Python 3.11+

## Installation (quick reference)

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

## CLI usage (reference)

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
