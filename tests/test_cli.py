"""Tests for CLI argument usability and player input resolution."""

from __future__ import annotations

from pathlib import Path

import pytest

from rp_foundry import cli
from rp_foundry.cli import _read_player_input, build_parser


def test_read_player_input_accepts_inline_text() -> None:
    result = _read_player_input("Scout the ruins.", None)
    assert result == "Scout the ruins."


def test_read_player_input_reads_file(tmp_path: Path) -> None:
    input_file = tmp_path / "player_input.txt"
    input_file.write_text("Search for the beacon lens", encoding="utf-8")

    result = _read_player_input(None, str(input_file))
    assert result == "Search for the beacon lens"


def test_read_player_input_rejects_both_forms() -> None:
    with pytest.raises(ValueError, match="Use only one"):
        _read_player_input("A", "input.txt")


def test_parser_requires_one_player_input_form() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(["build-packet", "--campaign", "demo"])

    args = parser.parse_args(
        ["build-packet", "--campaign", "demo", "--player-input", "Inline content"]
    )
    assert args.player_input == "Inline content"
    assert args.player_input_file is None


def test_main_returns_clean_error_for_missing_player_input_file(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "rp-foundry",
            "build-packet",
            "--campaign",
            "example_campaign",
            "--player-input-file",
            "does-not-exist.txt",
        ],
    )
    assert cli.main() == 2
