"""Tests for deterministic section selection."""

from rp_foundry.selection import select_relevant_sections


def test_select_relevant_sections_orders_by_score_then_index() -> None:
    content = """
# Intro
The city has a harbor and a guild.

# Rivals
A rival guild seeks the ancient key.

# Side Note
Merchants complain about tariffs.
"""
    player_input = "I want to find the rival guild and get the ancient key"

    result = select_relevant_sections(content, player_input, max_sections=2)

    assert len(result) == 2
    assert "Rivals" in result[0]
    assert "Intro" in result[1]


def test_select_relevant_sections_returns_empty_when_no_keywords() -> None:
    content = "# Note\nNothing useful here"
    result = select_relevant_sections(content, "to be or as")
    assert result == []
