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


def test_read_player_input_rejects_empty_file(tmp_path: Path) -> None:
    input_file = tmp_path / "player_input.txt"
    input_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="file is empty"):
        _read_player_input(None, str(input_file))


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


def test_parser_rejects_both_player_input_forms() -> None:
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "build-packet",
                "--campaign",
                "demo",
                "--player-input",
                "Inline content",
                "--player-input-file",
                "input.txt",
            ]
        )


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


def test_main_missing_player_input_flags_shows_argparse_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "rp-foundry",
            "build-packet",
            "--campaign",
            "example_campaign",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2
    stderr = capsys.readouterr().err
    assert "one of the arguments --player-input --player-input-file is required" in stderr
    assert "Traceback" not in stderr


def test_main_rejects_both_player_input_flags_with_no_traceback(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "rp-foundry",
            "build-packet",
            "--campaign",
            "example_campaign",
            "--player-input",
            "Inline",
            "--player-input-file",
            "campaigns/example_campaign/inputs/player_input.txt",
        ],
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main()

    assert exc_info.value.code == 2
    stderr = capsys.readouterr().err
    assert "not allowed with argument --player-input" in stderr
    assert "Traceback" not in stderr


def test_main_missing_player_input_file_prints_clean_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
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
    stderr = capsys.readouterr().err
    assert "Error: Player input file not found" in stderr
    assert "Traceback" not in stderr


def test_main_empty_player_input_file_prints_clean_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    input_file = tmp_path / "empty-player-input.txt"
    input_file.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "rp-foundry",
            "build-packet",
            "--campaign",
            "example_campaign",
            "--player-input-file",
            str(input_file),
        ],
    )

    assert cli.main() == 2
    stderr = capsys.readouterr().err
    assert "Error: Player input file is empty" in stderr
    assert "Traceback" not in stderr


def test_main_build_packet_missing_required_campaign_inputs_is_clean_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    campaign_root = tmp_path / "campaigns" / "missing_inputs"
    (campaign_root / "inputs").mkdir(parents=True)

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "sys.argv",
        [
            "rp-foundry",
            "build-packet",
            "--campaign",
            "missing_inputs",
            "--player-input",
            "Scout the road.",
        ],
    )

    assert cli.main() == 2
    stderr = capsys.readouterr().err
    assert "Error: Missing required input files:" in stderr
    assert "current_state.txt" in stderr
    assert "style_bible.txt" in stderr
    assert "campaign_bible.txt" in stderr
    assert "Traceback" not in stderr
