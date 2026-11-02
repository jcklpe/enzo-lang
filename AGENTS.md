# Agent Instructions
Enzo is an exploratory language and toy interpreter. Read [README](README.md) for the author's design intent.

## Agent policies
Read the project-owned [agent policy index](docs/agent-policies/policy.index.md) for status and scope. Load applicable adopted records and their complete prerequisite closures through that index. The three adopted kernel policies govern policy work; package updates do not adopt bundled candidates for Enzo.

Use the task-specific [Create](project-workflows/create-agent-policy/SKILL.md), [Edit](project-workflows/edit-agent-policy/SKILL.md), [Review](project-workflows/review-agent-policies/SKILL.md), [Adopt](project-workflows/adopt-agent-policies/SKILL.md) and [Retire](project-workflows/retire-agent-policy/SKILL.md) procedures. The [supplemental Copilot instructions](.github/copilot-instructions.md) remain applicable, including their test/golden-file approval boundary.

## Project workflows
This repository adopts the complete [Project Workflows](project-workflows/README.md) collection. Read [workflow.toml](project-workflows/workflow.toml), then load `project-workflows/<skill-name>/SKILL.md` before global seeds. The child branch is `project/enzo-lang`; the parent retains its own branch. The parent gitlink records the exact revision. Use [update-project-workflows](project-workflows/update-project-workflows/SKILL.md) for future reconciliation.

Actual documents stay here: `TODO.md` is the canonical coordination index, combining the retained language roadmap and deferred spike links. Existing syntax explorations stay in `scratchpad-syntax-features/`. Spike pairs use `docs/active-spikes/`; new captured or parked subjects may use individual `docs/scratch/` notes. [Preserve exploratory intent](docs/agent-policies/PRESERVE-EXPLORATION-preserve-exploratory-intent.md) governs the retained roadmap, deferred work and existing locations.

Use [Coordinate Project Contribution](project-workflows/coordinate-project-contribution/SKILL.md) to start contribution and review work under this project’s existing human direction. Each agent keeps its own spike; a branch may carry several spikes/issues and later reviews. Existing privacy, validation and publication rules remain authoritative.

## Changes and validation
Follow [Preserve concurrent work and Git boundaries](docs/agent-policies/PRESERVE-WORK-preserve-concurrent-work-and-git-boundaries.md) and [Validate changes with their owning instructions](docs/agent-policies/VALIDATE-CHANGES-validate-changes-with-their-owning-instructions.md).
