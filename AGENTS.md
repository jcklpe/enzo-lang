# Agent Instructions
Enzo is an exploratory language and toy interpreter. Read README for the author's design intent; do not turn syntax sketches or deferred ideas into implementation requirements. Preserve existing code, examples, and project vocabulary.

## Project workflows
This repository adopts the complete [Project Workflows](project-workflows/README.md) collection. Read [workflow.toml](project-workflows/workflow.toml), then load `project-workflows/<skill-name>/SKILL.md` before global seeds. The child branch is `project/enzo-lang`; the parent retains its own branch. The parent gitlink records the exact revision. Use [update-project-workflows](project-workflows/update-project-workflows/SKILL.md) for future reconciliation.

Actual documents stay here: `TODO.md` is the canonical coordination index, combining the retained language roadmap and deferred spike links. Preserve the roadmap context; inclusion is not approval to implement it. Existing syntax explorations stay in `scratchpad-syntax-features/`. Spike pairs use `docs/active-spikes/`; new captured or parked subjects may use individual `docs/scratch/` notes. Preserve existing locations and notes without bulk migration. A deferred spike or captured idea is not authorization to resume implementation.

## Changes and validation
Inspect current status and full selected diffs; preserve unrelated staged, unstaged, and untracked work. Make authorized local checkpoints by explicit pathspec under [commit-work](project-workflows/commit-work/SKILL.md), checking ignores before adding new files. Do not push, rewrite history, add co-author trailers, or commit credentials/private configuration.

For documentation/workflow changes, validate links, frontmatter, configuration, ancestry, and exact submodule pins. Inspect the current implementation's own test instructions before code changes; no new runtime/build process is established by this adoption. Keep prose paragraphs on single lines and avoid unrelated reformatting.
