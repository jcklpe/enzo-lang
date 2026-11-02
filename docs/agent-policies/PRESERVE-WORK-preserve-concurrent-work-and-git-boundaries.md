---
id: PRESERVE-WORK
type: operational
scope: "Agent edits and local checkpoints in this Enzo checkout."
status: proposed
authority: ""
revised: "2026-11-02"
depends_on: ["ADOPT-POLICIES"]
related_to: []
---
# Preserve concurrent work and Git boundaries
Inspect current status and full selected diffs; preserve unrelated staged, unstaged, and untracked work. Make authorized local checkpoints by explicit pathspec under [Commit Work](../../project-workflows/commit-work/SKILL.md), checking ignores before adding new files. Do not push, rewrite history, add co-author trailers, or commit credentials/private configuration.
