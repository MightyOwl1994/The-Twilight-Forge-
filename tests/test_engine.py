"""Tests for packet assembly behavior."""

from pathlib import Path

from rp_foundry.engine import build_packet
from rp_foundry.io_utils import resolve_campaign_paths


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_packet_includes_required_and_matching_optional(tmp_path: Path) -> None:
    campaigns = tmp_path / "campaigns"
    campaign_name = "test_campaign"
    paths = resolve_campaign_paths(campaign_name, campaigns_root=campaigns)

    _write(paths.inputs / "current_state.txt", "Current state text")
    _write(paths.inputs / "style_bible.txt", "Style rule text")
    _write(paths.inputs / "campaign_bible.txt", "Campaign rule text")
    _write(paths.inputs / "lore_appendix.txt", "# Relic\nThe sun relic is hidden under the tower.")

    result = build_packet(paths=paths, player_input="Let's search for the sun relic", packet_label="unit")
    packet_text = result.path.read_text(encoding="utf-8")

    assert "## Current State" in packet_text
    assert "## Style Bible" in packet_text
    assert "## Campaign Bible" in packet_text
    assert "## Lore Appendix (Selected)" in packet_text
    assert "sun relic" in packet_text.lower()


def test_build_packet_raises_on_missing_required(tmp_path: Path) -> None:
    campaigns = tmp_path / "campaigns"
    paths = resolve_campaign_paths("broken_campaign", campaigns_root=campaigns)
    _write(paths.inputs / "style_bible.txt", "x")

    try:
        build_packet(paths=paths, player_input="hello")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError as exc:
        assert "current_state.txt" in str(exc)
