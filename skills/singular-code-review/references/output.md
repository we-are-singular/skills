# Output Reference

Use a findings-first report. Keep it concise enough for a PR author to act on, but include enough evidence that a reviewer can verify each issue.

## Review Flags

- `critical` - must fix: exploitable vulnerability, data loss/corruption, complete outage, irreversible migration breakage, or a change that cannot safely land.
- `high` - should fix: likely user-facing bug, broken contract, authz/authn gap, serious regression, unsafe rollout, or major architecture mismatch.
- `low` - should fix: concrete reachable defect, contract problem, missing behavioral proof, performance risk, or material structural debt with meaningful present impact. A human may accept it with a reason, but the reviewer does not consider it optional.
- `question` - needs a human decision: specific unresolved intent or behavior whose answer is required before merge readiness can be decided.
- `nit` - optional cleanup: concrete touched-code improvement in naming, placement, commentary, readability, redundant types, or unused surface that is safe to leave unchanged.

## Report Shape

```markdown
## Findings

1. [high] Short finding title - `path/to/file.ts:42`
   Evidence: <diff line plus surrounding code/docs/intent source>
   Impact: <observable consequence>
   Fix: <concrete code change, refactor path, or decision needed>

2. [question] Active contracts disagree on compatibility - `path/to/file.ts:10`
   Evidence: <PR body/plan/conversation conflicts with tests or another active contract>
   Impact: <why the answer changes merge readiness>
   Ask: <specific contract decision needed>

## Intent Fit

- Intent source: <conversation | PR body | plan | inferred from commits | missing>
- Summary: <2-3 lines>
- Mismatches: <none or bullets>

## Review Coverage

- Scope: <base/range/PR, files, line count>
- Context read: <AGENTS/docs/plans/nearby code/tests>
- Review lanes: <subagents or sequential lanes>
- Not covered: <generated files, migrations not run, CI unavailable, remote ref unavailable>
- Residual risks: <bullets or none>
- Testing gaps: <bullets or none>

## TLDR

<Plain-language recommendation: what to do next, what to fix first, whether the shape is fine, or whether the work needs a structural rethink. Do not decide for the human.>
```

If there are no findings:

```markdown
## Findings

No findings.

## Review Coverage

- Scope: <...>
- Context read: <...>
- Residual risks: <...>
- Testing gaps: <...>

## TLDR

No review findings. Residual risks are listed above.
```

## Finding Rules

- Findings lead. Do not start with praise or a broad summary.
- Order by flag, then file path. Flag order is `critical`, `high`, `low`, `question`, `nit`.
- Each finding needs a file and line. If the issue is missing docs/intent, cite the most relevant changed file or PR body/plan location.
- Use absolute certainty sparingly. Say what was verified and what remains uncertain.
- Questions are findings only when a known contract fork blocks merge readiness. Name the exact decision, conflicting or missing evidence, and why the answer changes the review.
- Separate residual risks from actionable findings.
- Separate pre-existing issues unless the diff makes them newly reachable.

## TLDR Guidance

- Use `TLDR`. The reviewer recommends; humans decide.
- Keep it to one short paragraph or 2-4 bullets.
- Name the next move: fix specific items, split the PR, add intent/tests, rethink the structure, or proceed with residual risks.
- If findings are mostly questions or nits, say whether the next step is clarification or optional cleanup.
- If there are no findings, say no findings and mention any residual risk or missing validation.
