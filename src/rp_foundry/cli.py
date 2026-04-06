"""CLI entrypoint for rp-foundry."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rp_foundry.engine import build_packet, draft_update, log_scene
from rp_foundry.io_utils import check_health, read_text, read_yaml, resolve_campaign_paths


def _read_scene_text(scene_file: Path | None, scene_text: str | None) -> str:
    """Read scene text from either a file path or direct argument."""
    if scene_file:
        return read_text(scene_file)
    if scene_text:
        return scene_text.strip()
    raise ValueError("Provide either --scene-file or --scene-text.")


def _read_player_input(player_input: str | None, player_input_file: str | None) -> str:
    """Resolve player input from either raw text or file path.

    Raises:
        ValueError: if both or neither input forms are provided.
        FileNotFoundError: if a file path is provided but missing.
    """
    if player_input and player_input_file:
        raise ValueError("Use only one of --player-input or --player-input-file, not both.")

    if player_input:
        text = player_input.strip()
        if not text:
            raise ValueError("--player-input was provided but empty. Add text or use --player-input-file.")
        return text

    if player_input_file:
        file_path = Path(player_input_file)
        if not file_path.exists():
            raise FileNotFoundError(
                f"Player input file not found: {file_path}. "
                "Use --player-input for inline text or provide a valid file path."
            )
        return read_text(file_path)

    raise ValueError("Missing player input. Provide --player-input or --player-input-file.")


def cmd_build_packet(args: argparse.Namespace) -> int:
    """CLI handler for build-packet."""
    paths = resolve_campaign_paths(args.campaign)
    config = read_yaml(paths.config)
    player_input = _read_player_input(args.player_input, args.player_input_file)

    result = build_packet(paths=paths, player_input=player_input, packet_label=args.label)
    print(f"Built packet: {result.path}")
    if config:
        print(f"Campaign config loaded ({len(config)} keys).")
    if result.included_optional_sections:
        print("Included optional files:")
        for file_name, sections in result.included_optional_sections.items():
            print(f"  - {file_name}: {len(sections)} chunk(s)")
    return 0


def cmd_log_scene(args: argparse.Namespace) -> int:
    """CLI handler for log-scene."""
    paths = resolve_campaign_paths(args.campaign)
    scene_text = _read_scene_text(Path(args.scene_file) if args.scene_file else None, args.scene_text)
    log_path = log_scene(paths=paths, scene_text=scene_text, source_packet=args.source_packet)
    print(f"Logged scene: {log_path}")
    return 0


def cmd_draft_update(args: argparse.Namespace) -> int:
    """CLI handler for draft-update."""
    paths = resolve_campaign_paths(args.campaign)
    scene_text = _read_scene_text(Path(args.scene_file) if args.scene_file else None, args.scene_text)
    draft_path = draft_update(paths=paths, scene_text=scene_text, review_label=args.label)
    print(f"Created draft update: {draft_path}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """CLI handler for status."""
    paths = resolve_campaign_paths(args.campaign)
    health = check_health(paths)
    config_exists = paths.config.exists()

    print(f"Campaign: {args.campaign}")
    print(f"Config: {'present' if config_exists else 'missing'} ({paths.config})")
    print(f"Inputs: {paths.inputs}")
    print(f"Outputs: {paths.outputs}")
    print(f"Logs: {paths.logs}")

    if health["missing_required"]:
        print("Missing required inputs:")
        for file_name in health["missing_required"]:
            print(f"  - {file_name}")
    else:
        print("All required inputs are present.")

    if health["present_optional"]:
        print("Optional inputs available:")
        for file_name in health["present_optional"]:
            print(f"  - {file_name}")

    output_count = len(list(paths.outputs.glob("*.txt"))) if paths.outputs.exists() else 0
    log_count = len(list(paths.logs.glob("*.txt"))) if paths.logs.exists() else 0
    print(f"Output artifacts: {output_count}")
    print(f"Scene logs: {log_count}")
    return 0 if not health["missing_required"] else 1


def build_parser() -> argparse.ArgumentParser:
    """Build argparse parser for rp-foundry commands."""
    parser = argparse.ArgumentParser(prog="rp-foundry", description="Roleplay context packet tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    packet_parser = subparsers.add_parser("build-packet", help="Build a curated scene packet")
    packet_parser.add_argument("--campaign", required=True, help="Campaign folder name")
    input_group = packet_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--player-input",
        help="Raw player input text (example: --player-input \"I interrogate the courier\")",
    )
    input_group.add_argument(
        "--player-input-file",
        help="Path to player input text file (example: campaigns/<campaign>/inputs/player_input.txt)",
    )
    packet_parser.add_argument("--label", help="Optional label for output file name")
    packet_parser.set_defaults(func=cmd_build_packet)

    log_parser = subparsers.add_parser("log-scene", help="Log a completed scene output")
    log_parser.add_argument("--campaign", required=True, help="Campaign folder name")
    log_parser.add_argument("--scene-file", help="Path to a text file containing scene output")
    log_parser.add_argument("--scene-text", help="Direct scene output text")
    log_parser.add_argument("--source-packet", help="Optional source packet file name")
    log_parser.set_defaults(func=cmd_log_scene)

    update_parser = subparsers.add_parser("draft-update", help="Draft a suggested canon/state update")
    update_parser.add_argument("--campaign", required=True, help="Campaign folder name")
    update_parser.add_argument("--scene-file", help="Path to a text file containing scene output")
    update_parser.add_argument("--scene-text", help="Direct scene output text")
    update_parser.add_argument("--label", help="Optional label for draft file name")
    update_parser.set_defaults(func=cmd_draft_update)

    status_parser = subparsers.add_parser("status", help="Show campaign health and completeness")
    status_parser.add_argument("--campaign", required=True, help="Campaign folder name")
    status_parser.set_defaults(func=cmd_status)

    return parser


def main() -> int:
    """CLI program entrypoint."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
