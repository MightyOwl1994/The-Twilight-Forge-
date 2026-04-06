"""Core data models for rp-foundry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CampaignPaths:
    """Resolved paths for a single campaign directory."""

    root: Path
    inputs: Path
    outputs: Path
    logs: Path
    config: Path


@dataclass(frozen=True)
class PacketBuildResult:
    """Result data from packet construction."""

    path: Path
    included_optional_sections: dict[str, list[str]]
