# Decisions

Short record of important technical/product choices.

## 2026-04-07 — Keep architecture simple and file-based
**Decision:** Use a lightweight, deterministic CLI workflow with plain text files.

**Why:** Easier to understand, easier to debug, friendly for beginners, and safer for collaborative RP canon.

**Tradeoff:** Fewer advanced features in early versions.

## 2026-04-07 — Keep project setting-agnostic
**Decision:** The engine should stay reusable and not be permanently tied to Twilight.

**Why:** Makes it useful for other campaigns/settings and keeps long-term flexibility.

**Tradeoff:** We avoid lore-specific shortcuts in core logic.

## 2026-04-07 — Draft updates, don’t auto-apply
**Decision:** Generate update artifacts for review instead of writing directly into canon/state files.

**Why:** Protects canon quality and keeps humans in the review loop.

**Tradeoff:** One extra manual review step after sessions.

## Update this file when
- You make a choice that changes architecture, workflow, or scope
- You reject a major approach and want a reminder of why
