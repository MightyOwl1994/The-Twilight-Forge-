"""File-system and text IO utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rp_foundry.models import CampaignPaths


REQUIRED_INPUTS = ("current_state.txt", "style_bible.txt", "campaign_bible.txt")
OPTIONAL_INPUTS = (
    "lore_appendix.txt",
    "roster_threads.txt",
    "open_threads.txt",
    "recent_summary.txt",
)


def resolve_campaign_paths(campaign_name: str, campaigns_root: Path = Path("campaigns")) -> CampaignPaths:
    """Return resolved standard paths for a campaign."""
    root = campaigns_root / campaign_name
    return CampaignPaths(
        root=root,
        inputs=root / "inputs",
        outputs=root / "outputs",
        logs=root / "logs",
        config=root / "config.yaml",
    )


def ensure_dirs(paths: CampaignPaths) -> None:
    """Create missing output/log directories."""
    paths.outputs.mkdir(parents=True, exist_ok=True)
    paths.logs.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    """Read UTF-8 text from disk."""
    return path.read_text(encoding="utf-8").strip()


def read_yaml(path: Path) -> dict[str, Any]:
    """Read a minimal YAML mapping from disk.

    This parser intentionally supports a conservative subset used by V1 config:
    top-level `key: value` lines and simple one-level indentation.
    Unknown/complex constructs are treated as raw strings.
    """
    if not path.exists():
        return {}

    result: dict[str, Any] = {}
    current_parent: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if indent == 0:
            if value:
                result[key] = value
                current_parent = None
            else:
                result[key] = {}
                current_parent = key
        elif current_parent:
            parent = result.get(current_parent)
            if isinstance(parent, dict):
                parent[key] = value

    return result


def check_health(paths: CampaignPaths) -> dict[str, list[str]]:
    """Return missing and present files summary for campaign status."""
    missing_required: list[str] = []
    present_optional: list[str] = []

    for file_name in REQUIRED_INPUTS:
        if not (paths.inputs / file_name).exists():
            missing_required.append(file_name)

    for file_name in OPTIONAL_INPUTS:
        if (paths.inputs / file_name).exists():
            present_optional.append(file_name)

    return {
        "missing_required": missing_required,
        "present_optional": present_optional,
    }
