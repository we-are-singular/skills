# proof

A Claude Code plugin returns evidence of work done.

- **Skill** (`skills/proof/SKILL.md`) tells the agent when to collect evidence and how.
- **CLI** (`skills/proof/scripts/proof`, Python 3 standard library only) stores the evidence and writes `PROOF.md`.
- **Stop hook** (`hooks/hooks.json`) stops the agent from ending its turn while a proof is open and not built.

## Install

Needs `python3` (3.9 or newer) and `git` on your PATH.

As a Claude Code plugin, with the skill, the CLI and the Stop hook:

```
/plugin marketplace add we-are-singular/skills
/plugin install proof@singular
```

As a standalone skill, with the skill and the CLI but no Stop hook:

```sh
npx skills add we-are-singular/skills --skill proof
```

To try a local checkout without installing:

```sh
claude --plugin-dir <path to this folder>
```

## Flow

```sh
proof start "Fix the login redirect"            # before step on by default
proof add before --cmd "npm test -- login" --caption "Login test fails" --key login
# ...change the code...
proof add after  --cmd "npm test -- login" --caption "Login test passes" --key login
proof unproven "Safari not checked"
proof build --summary "Login now returns you to the page you came from."
```

If the change came before the proof, `proof add before --in <dir>` runs the command in a temporary worktree at the old commit while the proof stays here.

Output goes to `.proof/<stamp>-<slug>/` at the worktree root: `proof.json`, `files/` and `PROOF.md`. `.proof/` ignores itself in git.

## Skipping the before step

`proof start` decides once per proof, in this order:

1. `--no-before` or `--before`
2. `PROOF_BEFORE=off` or `on` in the environment
3. `{"before": false}` in `.proof/config.json`
4. On

With the before step off, `proof add before` is refused, the hook and `build` ask only for after evidence, and `PROOF.md` drops the Before and After labels.

## Rules

`proofkit/rules.py` holds every completeness rule. `build` and the Stop hook both use it.

- With the before step on, the proof needs at least one before item.
- It needs at least one after item.
- Every before key needs an after with the same key.
- Before evidence is refused once any after evidence exists.

## Gaps

- One open proof per worktree. Two sessions in the same worktree share the `current` pointer. Separate worktrees don't.
- The hook only checks proofs started with `proof start`. It doesn't decide which work needs one.
- Evidence is whatever the agent captures. The CLI records the commit and whether the tree was dirty, but it doesn't check that a before item ran on unchanged code.
