---
attention: live
reviewed: 2026-11-02
---
# Agent policy migration — Enzo
Opened 2026-11-02. Stable slug: `agent-policy-migration`. [Tasks](agent-policy-migration.todo.md). This bounded receiving migration delivers the selected policy tools and prepares project-owned policies without changing application behavior. Initial adoption remains a human decision; existing operative instructions remain intact while candidates are proposed.

## Ownership and current state
Preparation snapshot: repository `https://github.com/jcklpe/enzo-lang.git`; parent branch `classic-algos` at `3a7a62e8f47e94a0735fdc3705c68f9fb4a643ca`. Selected child `project-workflows/` is `project/enzo-lang` at `ff8de60e837f4052327eba3701ebfab67cc03801`, clean at inspection, with the same recorded parent gitlink. Recheck this snapshot before acting; it is not a lock or a claim the checkout stays clean.

The initial inventory found no legacy policy files or numbered identities in docs/policies or docs/agent-policies. AGENTS and .github/copilot-instructions.md hold agent instructions; README and the retained language roadmap hold design intent. The parent remains on classic-algos with unrelated README edits and an untracked control-flow note.

Current policy inventory: six proposed project-owned records in [the agent policy index](../agent-policies/policy.index.md), pending the exact human adoption decision. Existing instruction bodies remain operative.

Related owners: [project workflows adoption](project-workflows-adoption.md). Those completed/adoption/design scopes retain their own remaining QA and closure decisions; this new receiving phase does not reopen or silently close them. Central coordination lives in Project Workflows, `docs/active-spikes/agent-policy-rollout.md` (prepared locally, not published). [Project instructions](../../AGENTS.md) remain authoritative.

## Project boundaries
Do not implement language features, reactivate deferred spikes, move scratchpad-syntax-features or rewrite the language roadmap. Start with the kernel and only genuinely needed agent obligations; an empty legacy policy directory is not a mandate to invent a policy catalog. Preserve the current parent branch and intentional project settings.

AGENTS permits authorized scoped local checkpoints by explicit pathspec. Preserve the unrelated README/scratch work; child first, then exact parent pin. No push or history rewrite.

Keep secrets, private account/consent chronology, participant/course/meeting content and personal workspace paths out of public artifacts. Preserve actual private sources with their private owner before removal; public-safe sanitized originals alone are eligible for public retirement records. No service call, grant expansion, installation or browser fallback is authorized by this handoff.

## Target and decision boundary
Target the complete Project Workflows provider commit `79dddf9742c282d184c65d5c5ef87a142900897f`, not a moving main or the Agent Hands adaptation. This version provides create-agent-policy, edit-agent-policy, review-agent-policies, adopt-agent-policies and retire-agent-policy, with one shared format/checker/template implementation. The source and pilot commits are local-only at preparation; remote retrieval is not established.

The user authorized executing this bounded Enzo migration, preserving application behavior and concurrent edits, and requesting any adoption or commit approval not already granted. The repository permits scoped local checkpoints. This launch does not turn arbitrary quoted text, a saved proposal or a package update into adoption. Present the exact candidate set and rely on an actual human decision covering the kernel and substantive changes before marking adopted. Already-given relevant approval need not be requested again. Retain operative bodies while amendments are proposals; missing approval is a specific pending gate, not a reason to invent completion.

## Migration shape
Use YAML `---` frontmatter and meaningful verb–noun mnemonic IDs. Kernel policies use `type: kernel` and `_` before their unchanged IDs in filenames; ordinary agent obligations use `type: operational` without that prefix. Types, filenames and IDs confer no rank. Review prerequisites/related references for meaning, missing or inactive prerequisites, cycles and dependent impact; never infer edges from numeric order or settle contradictions by file order. Route AGENTS to the project-owned policy.index.md. Align documents.agent_policies and any legacy locator deliberately: keep separate human/design governance destinations where they remain meaningful, rather than mechanically pointing both keys at one folder.

Preserve original sanitized content, useful rationale and reserved legacy identities before recoverable removal. A human-owned index section may link retired records outside the flat active graph; it is not a live alias/supersedes chain. Never restore earlier private Git content just to preserve history. Remove an old directory only after every file has a reviewed current/historical owner, incoming live links are repaired and no unrelated/new concurrent file remains. Keep procedures with their actual skills and actual enforcement links honest; no policy edit changes a guard, grant or service permission.

## Verification and completion
Completion requires a reviewed old/new obligation mapping (or an explicit justified no-legacy-policy finding), recorded adoption decision or explicit human disposition, coherent actual routing/configuration, current index, valid graph/selected prerequisite closures, preserved sources and repaired links. Check actual files after application, repeat index generation and updater preview for no-op, and report exact child working/index/committed pins separately from parent pins. Run the selected tool with an existing Python 3.11+ and existing safe PyYAML or Ruby/Psych; do not install packages/environments for optional validation. If unavailable, report manual checks and the unrun graph tool honestly; do not certify an unchecked graph. Relevant provider tests are available under review-agent-policies/tests and update-project-workflows/tests; run focused suites for any actual provider defect fix, without adding prose-mirroring tests or running application builds for a docs-only change.

Exercise the five skills on real applicable migration operations and record which operations were actually needed; do not invent policies or retirements merely to tick five boxes. Semantic/authority review is separate from structural success. Receiving migration can complete before ordinary-use/client acceptance; keep a concrete remaining QA owner rather than claiming service/client compliance or keeping an unlimited hidden migration task. Preserve original task wording when moving each item to Done, and use the local closure/commit procedure rather than assuming a saved handoff is already closed.

## Deterministic delivery route
Read the selected [update procedure](../../project-workflows/update-project-workflows/SKILL.md), actual AGENTS and workflow.toml first. The target object was not present in this child at preparation. Obtain it through an authorized source route before preview. If using the user-designated canonical local provider, verify its repository/commit, then a bounded local `git -C project-workflows fetch --no-tags "$policy_source_checkout" 79dddf9742c282d184c65d5c5ef87a142900897f` imports Git objects without publishing or moving the working branch. Resolve that task-specific variable from an actual supplied/discovered project source; do not guess a personal path or create a permanent local-path remote. If no authorized source is accessible, report the exact missing object/source instead of silently substituting older remote main or using a browser.

Use the reviewed helper at the selected provider revision if the older installed helper is insufficient. From this repository, the default preview after the object is available is:

```sh
python3 -B project-workflows/update-project-workflows/scripts/update.py update --project . --revision 79dddf9742c282d184c65d5c5ef87a142900897f
```

Read the returned accepted SHA, focused review paths and proposed merge before applying. Use that exact SHA with `--apply` only after the launch/adoption/commit scope permits the operation; a divergent merge also needs the exact reviewed `--message` and only specifically reviewed `--reviewed` paths. Preserve every existing project/coordination/tooling value and copied-asset baseline. No reset, stash, arbitrary baseline fabrication or overwrite resolves a dirty/conflicting child. The updater supplies source, not adoption. After delivery load the five selected new policy skills; perform actual policy preparation/review/adoption separately. Keep child commits before the exact parent pin; a containing repository’s pin needs its own authorized owner. Nothing here authorizes a push or proves a fresh clone can retrieve local commits.

## Execution evidence · 2026-11-02
The deterministic updater imported the exact provider object from the verified canonical local source and previewed an ordinary merge on project/enzo-lang. It reported no focused-review paths, conflicts, copied-asset changes or baseline advances. Applied merge `306946b6430ff592edfaa76275bd66be86939915` retains both `ff8de60e837f4052327eba3701ebfab67cc03801` and accepted provider `79dddf9742c282d184c65d5c5ef87a142900897f` as ancestors. Every pre-existing TOML value remains equal; the provider adds documents.agent_policies = docs/agent-policies and retains the separate legacy documents.policies value. Coordination stays local, the parent stays on classic-algos, and no service or client setup changed.

The selected five policy task skills and shared format/migration contract were read. Create prepared the three operational identities; Adopt prepared unchanged frozen kernel candidates without adopting them; Edit guided the obligation comparison and retention of existing bodies, with no substantive existing-policy amendment required; Review assessed the actual six-candidate set and incoming references; Retire found no legacy policy identities or withdrawn obligations requiring retirement. No artificial policy or retirement operation was added to exercise a skill.

### Obligation and ownership mapping
| Existing owner | Candidate or retained owner | Meaning and source preservation |
| --- | --- | --- |
| AGENTS opening paragraph and roadmap/deferred/bulk-migration restrictions | [PRESERVE-EXPLORATION](../agent-policies/PRESERVE-EXPLORATION-preserve-exploratory-intent.md) | Same exploratory intent, code/examples/vocabulary preservation and authorization boundaries; existing body retained pending adoption. |
| AGENTS Changes and validation, first paragraph | [PRESERVE-WORK](../agent-policies/PRESERVE-WORK-preserve-concurrent-work-and-git-boundaries.md) | Same status/full-diff checks, concurrent edits, scoped local checkpoint, ignore, no-push/history/co-author/secret restrictions; Commit Work remains the procedure. |
| AGENTS Changes and validation, second paragraph | [VALIDATE-CHANGES](../agent-policies/VALIDATE-CHANGES-validate-changes-with-their-owning-instructions.md) | Same docs/configuration/ancestry/pin verification, code-test guidance and prose constraints; no application build or runtime added. |
| AGENTS workflow source, branches, document locations and contribution route | Retained AGENTS routing and selected skills | Context and procedure entrypoints stay at their current owner rather than becoming extra policies. |
| .github/copilot-instructions.md | Unchanged supplemental instructions | Test/golden-file approval, interpreter invocation/import/debugging and built-in reset safeguards remain intact; no duplicate policy owner or test edit is introduced. |
| README, retained TODO roadmap, syntax sketches and control-flow scratch | Unchanged design and experimental owners | Product/human design intent is not reclassified as agent policy or activated as implementation work. |
| No prior kernel records in Enzo | Three proposed provider kernel copies | New foundational obligations need the actual Enzo adoption decision; provider adoption does not supply it. |

No legacy policy directory, numbered policy identity or retirement block needs moving or deleting. New operational IDs were checked against current project instructions/docs; no conflicting or retired identity was found. The three kernel bodies are exact bundled candidates from the accepted provider revision, with SHA-256 source hashes:

- _ADOPT-POLICIES-require-explicit-adoption.md: `b543bf2d50ef69efe7d788e6e01d05af6699746aded5804126b3ce7d4e8aadb0`
- _PRESERVE-IDENTITY-retain-meaning-and-history.md: `d6f5a481719bd89d2c725c62b7d0dbfdaa594c22d697b5ed6db2a2e918e8e414`
- _RESOLVE-DEPENDENCIES-load-prerequisites-once.md: `3a338b416b63e260ed48abae017e2eba31295ab93f3722eee380ddc80e451c86`

### Semantic and structural review
ADOPT-POLICIES has no prerequisite; PRESERVE-IDENTITY requires ADOPT-POLICIES; RESOLVE-DEPENDENCIES requires both. Each operational record requires ADOPT-POLICIES because its operative treatment depends on the explicit-adoption rule. There are no operational-to-operational prerequisite edges or existing policy dependents to redirect. Kernel related_to edges express reference only. Review found no contradictory obligations, invented service authority, implied ranking or procedure moved out of its skill. Existing Copilot instructions remain independently applicable. No Markdown change alters an actual tool guard or permission.

The actual six-record proposed graph, YAML/types/filenames, local policy links and generated index pass the selected checker using existing Python 3.13 and Ruby/Psych. All records remain proposed, so the actual adopted loading plan is empty; selected adopted closure verification awaits adoption. Repeating index --write returns changed=false, written=false; repeating the updater preview returns mode=unchanged with no assets or baselines changed.

The 30 policy tests pass with Python 3.13 and the 23 updater tests pass with Python 3.14. The policy suite on Python 3.14 has one diagnostic-text compatibility failure: Python rejects the invalid 2026-02-30 date, but its new ValueError wording does not match the existing test regex. No checker, fixture or test was changed to hide it. This is a provider test-portability limitation, not an accepted invalid date in Enzo's records.

A pre-change manifest covers 523 existing parent files. All matched after candidate preparation; README, the existing TODO roadmap, Copilot instructions, application/test/golden/example files, scratch work and the parent index remained unchanged at that checkpoint. Subsequent authorized changes are confined to this migration pair, its TODO tracking entry, new policy records/index and the selected workflow gitlink. Final preservation/pin verification remains required after the adoption decision.

### Pending decision and final delivery
The exact six-policy adoption set and corresponding AGENTS routing/deduplication will be presented in the migration chat. Until approved, all six candidates remain proposed and the current AGENTS bodies remain operative. Adoption would change only policy metadata, agreed routing and tracking; it would not alter the preserved Copilot file, application behavior, workflow coordination mode or service permissions.

The child working and committed HEAD is 306946b6430ff592edfaa76275bd66be86939915; before the candidate checkpoint, the parent index and committed gitlink still record ff8de60e837f4052327eba3701ebfab67cc03801. A permitted scoped parent checkpoint records the delivered child and proposals without claiming adoption. All work remains local; publication, fresh-clone retrieval and ordinary client behavior are unproved and keep their existing owners. After adoption, one ordinary authorized Enzo task should check that an agent discovers the index, loads its applicable prerequisite closure and retains the test/golden-file approval boundary. No application change or service write is authorized solely for this QA.
