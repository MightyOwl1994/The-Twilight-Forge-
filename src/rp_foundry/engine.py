"""Packet assembly and scene logging services."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from rp_foundry.io_utils import OPTIONAL_INPUTS, REQUIRED_INPUTS, ensure_dirs, read_text
from rp_foundry.models import CampaignPaths, PacketBuildResult
from rp_foundry.selection import select_relevant_sections


def _timestamp() -> str:
    """Return a sortable UTC timestamp string."""
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def build_packet(paths: CampaignPaths, player_input: str, packet_label: str | None = None) -> PacketBuildResult:
    """Build and persist a curated scene packet."""
    ensure_dirs(paths)

    missing_required = [name for name in REQUIRED_INPUTS if not (paths.inputs / name).exists()]
    if missing_required:
        missing_display = ", ".join(missing_required)
        raise FileNotFoundError(f"Missing required input files: {missing_display}")

    included_optional_sections: dict[str, list[str]] = {}
    parts: list[str] = []

    parts.append("# SCENE PACKET")
    parts.append(f"Generated: {datetime.now(timezone.utc).isoformat()}")
    parts.append("")

    for file_name in REQUIRED_INPUTS:
        section_name = file_name.replace("_", " ").replace(".txt", "").title()
        parts.append(f"## {section_name}")
        parts.append(read_text(paths.inputs / file_name))
        parts.append("")

    for file_name in OPTIONAL_INPUTS:
        file_path = paths.inputs / file_name
        if not file_path.exists():
            continue

        selected = select_relevant_sections(read_text(file_path), player_input)
        if not selected:
            continue

        included_optional_sections[file_name] = selected
        section_name = file_name.replace("_", " ").replace(".txt", "").title()
        parts.append(f"## {section_name} (Selected)")
        for index, chunk in enumerate(selected, start=1):
            parts.append(f"### Chunk {index}")
            parts.append(chunk)
            parts.append("")

    parts.append("## Player Input")
    parts.append(player_input.strip())
    parts.append("")

    label = packet_label or _timestamp()
    packet_path = paths.outputs / f"packet-{label}.txt"
    packet_path.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")

    return PacketBuildResult(path=packet_path, included_optional_sections=included_optional_sections)


def log_scene(paths: CampaignPaths, scene_text: str, source_packet: str | None = None) -> Path:
    """Write a scene output entry into campaign logs."""
    ensure_dirs(paths)
    timestamp = _timestamp()
    log_path = paths.logs / f"scene-{timestamp}.txt"

    header = [
        "# Scene Log",
        f"Timestamp: {datetime.now(timezone.utc).isoformat()}",
    ]
    if source_packet:
        header.append(f"Source Packet: {source_packet}")
    header.append("")

    body = "\n".join(header) + scene_text.strip() + "\n"
    log_path.write_text(body, encoding="utf-8")
    return log_path


def draft_update(paths: CampaignPaths, scene_text: str, review_label: str | None = None) -> Path:
    """Create a non-destructive suggested state/canon update artifact."""
    ensure_dirs(paths)
    label = review_label or _timestamp()
    output_path = paths.outputs / f"update-draft-{label}.txt"

    template = f"""# Suggested Canon/State Update (Human Review Required)
Generated: {datetime.now(timezone.utc).isoformat()}

## Scene Outcome Summary
{scene_text.strip()}

## Proposed Current State Updates
- [ ] Add key state changes observed in this scene.
- [ ] Note unresolved consequences for future scenes.

## Proposed Canon Updates (Optional)
- [ ] If any long-term canon changed, describe it here.
- [ ] If no canon changes, mark as \"No canon updates\".

## Reviewer Notes
- [ ] Confirm facts with transcript before applying manually.
"""
    output_path.write_text(template, encoding="utf-8")
    return output_path
