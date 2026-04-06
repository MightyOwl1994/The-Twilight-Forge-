"""Deterministic section selection logic for optional context files."""

from __future__ import annotations

import re
from dataclasses import dataclass

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
}


@dataclass(frozen=True)
class ScoredSection:
    """A section and score for sorting and inclusion."""

    text: str
    score: int
    index: int


def tokenize(text: str) -> set[str]:
    """Convert text into normalized keyword tokens."""
    terms = {token.lower() for token in re.findall(r"[A-Za-z0-9_']+", text)}
    return {term for term in terms if term not in STOPWORDS and len(term) > 2}


def split_sections(text: str) -> list[str]:
    """Split freeform text into simple chunks by headings and blank lines."""
    lines = [line.rstrip() for line in text.splitlines()]
    sections: list[str] = []
    current: list[str] = []

    for line in lines:
        if line.startswith("#") and current:
            sections.append("\n".join(current).strip())
            current = [line]
            continue

        if not line.strip() and current:
            sections.append("\n".join(current).strip())
            current = []
            continue

        if line.strip():
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    return [chunk for chunk in sections if chunk]


def select_relevant_sections(content: str, player_input: str, max_sections: int = 3) -> list[str]:
    """Select relevant optional sections via keyword overlap.

    Selection is deterministic: sections are ranked by overlap score (descending),
    then by original section order (ascending).
    """
    input_terms = tokenize(player_input)
    if not input_terms:
        return []

    scored: list[ScoredSection] = []
    for idx, section in enumerate(split_sections(content)):
        overlap = len(tokenize(section) & input_terms)
        if overlap > 0:
            scored.append(ScoredSection(text=section, score=overlap, index=idx))

    scored.sort(key=lambda item: (-item.score, item.index))
    return [item.text for item in scored[:max_sections]]
