# AI development workflow

Use this cycle for feature tickets and bug fixes: explore, agree, implement, verify, review, close and hand off. Keep the record proportional to the task. A small fix can use a few bullets; a larger feature may need a separate plan.

The developer owns product decisions, approves the implementation scope, and merges PRs. AI investigates the code, recommends an approach, implements authorised work, and supplies verification evidence.

## 1. Explore and prepare the ticket

Read the ticket description and relevant discussion, then follow the [documentation index](../README.md) to the relevant product requirements, decisions, and implementation guidance. Treat proposed requirements and open questions as decisions to resolve, rather than settled behaviour. Flag any discrepancies between the repo documents and information supplied on the GitHub issue.

Inspect the affected code, callers, data models, and existing tests. Identify reusable functionality and trace the current behaviour across components. Distinguish what the docs intend from what the code currently does; check discrepancies against the source before drawing conclusions.

Present a concise exploration brief:

- The problem, current behaviour, and intended outcome.
- Scope and exclusions, with observable acceptance criteria.
- Relevant docs and code, including existing functionality to reuse.
- Recommended approach and meaningful alternatives or tradeoffs.
- Verification approach, dependencies, and unresolved decisions.
- Proposed ticket or PR splits and any recommended follow-ups.

For UI work, describe the user interaction and failure behaviour. For API or data changes, describe affected contracts, access rules, and migration needs. Investigate only what is relevant to the task.

**Ready to implement:** the developer has agreed to the brief, acceptance criteria are testable, blocking decisions are resolved, and the proposed PR fits the size guidance below. Exploration authorises inspection and recommendations. Wait for agreement before implementation unless the developer has already explicitly authorised the agreed scope.

Keep the existing issue as the task's scope and status record. Propose concise amendments when it lacks information; apply them when authorised. Create GitHub issues only when the developer asks. For work without an issue, use the same brief in the conversation or a saved plan.

## Ticket and PR size

Aim for one independently explainable, verifiable outcome per PR. Include the code, tests, migrations, and documentation needed for that outcome. Use focused commits that support it.

- Prefer roughly 100-300 changed lines of handwritten code. Smaller is fine.
- Above roughly 400 added plus deleted lines of handwritten code, propose a split before implementation or further expansion. Tests count; generated files and lockfiles do not count toward this budget, but still need appropriate review. Consider documentation volume separately.
- Also propose a split when there are independent acceptance criteria, unrelated concerns, several difficult decisions, or parts that could ship separately. Complexity can justify splitting a much smaller PR.
- Treat 400 lines as a review checkpoint, not a mechanical limit. If a larger change is more coherent, explain why and obtain agreement on the exception. Avoid artificial splits that leave broken behaviour or unsafe intermediate states.

Prefer small end-to-end slices when practical. A transport-selection change may need React, Flask, and tests in one PR. A separate algorithm rewrite or unrelated cleanup belongs in another task. When preparatory work needs its own PR, state the dependency order and how each intermediate state remains usable.

## Follow-up tickets

Recommend follow-ups during exploration and whenever implementation or review reveals a concrete need. For each, state the problem, evidence or affected code, why it belongs outside the current scope, and whether it blocks this task or can wait. Check existing issues for duplicates when available; otherwise flag that the duplicate check remains outstanding.

Fix defects introduced by the current change within its scope. Separate pre-existing defects and optional improvements unless they prevent meeting the acceptance criteria. Present useful follow-up recommendations at handoff, without automatically creating issues or expanding implementation.

## 2. Implement the agreed slice

Default to working in the primary repository checkout. Before starting a new task, check its branch and `git status --short`, including staged, unstaged, and untracked files.

- If the primary checkout is clean, create or switch to the task's feature branch there and proceed. Base independent work on the latest `origin/main`; use another base for an agreed dependency. Working in the primary checkout does not mean committing directly to `main`.
- If it has uncommitted changes, summarise the affected files and ask the developer whether to use a worktree, finish or otherwise resolve the existing changes first, or switch to a new branch carrying those changes. Wait for that choice before changing branches or files. Switching branches can carry uncommitted changes with it; it does not isolate them. Commit, stash, move, or discard existing changes only as agreed with the developer.
- Create or use a worktree only when the developer explicitly requests it for the task or PR. Put new worktrees under the primary checkout's gitignored `.worktree/` folder. From the primary checkout, use `git worktree add -b <branch> .worktree/<task-name> origin/main`, or `git worktree add .worktree/<task-name> <branch>` for an existing branch that is not checked out elsewhere.

Run edits, checks, commits, and pushes from the chosen checkout. Follow the repository's [setup and contribution guidance](../../README.md); a new worktree needs its own local configuration and dependencies. Preserve unrelated local changes and existing worktrees. Implement in focused increments and run relevant checks as work progresses.

Add meaningful tests for changed behaviour, failure cases, and regressions. Use existing test patterns where suitable. If a new dependency, architecture choice, blocker, or scope increase changes the agreed approach, present the decision and update the brief before doing the dependent work. Continue independent work where possible.

**Ready to verify:** the agreed slice is implemented, required supporting changes are included, and any scope changes have been agreed.

## 3. Verify the behaviour

Run the relevant commands from [README checks](../../README.md#checks). Map each acceptance criterion to an automated result or a specific manual check. Report commands, results, and anything not verified, with the reason. Distinguish pre-existing failures from regressions using evidence.

For pubPoint, verify affected journeys across React, Flask, and MySQL where needed. Depending on the task, check permissions, search-specific state versus saved defaults, retry behaviour, persistence, and migrations. Use controlled Maps responses where appropriate to keep tests repeatable and avoid unnecessary paid requests. Passing lint and build alone does not verify a user journey.

**Ready to review:** acceptance criteria have verification evidence, or remaining gaps are explicit for the developer to assess.

## 4. Review and resolve findings

Use a separate review pass, preferably a fresh session supplied with the agreed brief, relevant docs, the diff base, and verification results. Review the full change and affected code beyond the diff. Check behaviour against acceptance criteria, project conventions, and second-order effects on callers and data.

Report actionable defects and material risks with their impact and suggested fix. Keep optional design recommendations separate. A review request authorises inspection and recommendations; edit files only when changes are explicitly requested. After authorised fixes, rerun affected checks and review the changed areas.

Prepare the PR with the problem, resulting behaviour, relevant issue, verification evidence, and remaining limitations. Assess the final diff against the size guidance again.

**Ready to merge:** material findings are resolved or explicitly accepted, verification gaps are accepted, and the developer approves. AI never merges PRs in this repo.

## 5. Close and hand off

Deployment and release are not necessary until the MVP stage is reached.

Update canonical docs when behaviour or decisions change. Record durable architectural choices in [decision records](../decisions/README.md), implementation guidance under `development/`, and changed setup or verification commands in the README. Link these from the issue when one exists.

**Complete:** the agreed development target is reached, verification results and PR status are recorded, and follow-ups are visible. State whether the PR is ready for review, approved, or merged, and identify any remaining action for the developer.

## Compact task record

Use this structure in an existing ticket or exploration brief. Link to canonical docs instead of copying them. Omit fields that add no value for a small task.

```text
Outcome and current behaviour:
Context: issue, relevant docs, and code
Scope and exclusions:
Acceptance criteria:
Approach and decisions:
Verification:
Splits, dependencies, and follow-ups:
Status and next action:
```

Save separate working plans in `.ai/plans`. Keep the task record current enough that a fresh AI session can resume without relying on chat history.
