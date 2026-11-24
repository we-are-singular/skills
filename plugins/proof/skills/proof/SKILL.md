---
name: proof
description: Back a change with real before and after evidence in one PROOF.md. Use when the person says "prove it", "show me it works", "proof of work", "before and after", or asks you to prove, show or demonstrate that work is done, or when a task needs proof before handoff.
---

A proof is evidence from this work, captured now: screenshots, clips, command output, test runs. Each piece shows one claim, with a one-line caption. Anything the evidence doesn't show goes on the Not proven list.

Run the CLI as `python3 <this skill's folder>/scripts/proof`, written `proof` below. `proof --help` and `proof <command> --help` list every option.

## Steps

1. **Open.** Before you touch code, run `proof start "<task title>"`. Add `--no-before` when the person asks to skip the baseline, when the work has no prior state to show (a new file, a new page), or when the change is already made and the person didn't ask for a baseline. Done when `proof status` shows the proof open.
2. **Baseline** (before step on). Capture the current behaviour for each claim you plan to prove: `proof add before --cmd "<test or command>" --caption "<what it shows>" --key <claim>`, or `--file <screenshot>`. Done when every claim has before evidence and no code has changed yet. `proof` refuses before evidence once after evidence exists.

   If the change is already made and the person asks for a baseline, rebuild the old state in a temporary worktree and leave this one untouched: `git worktree add --detach <tmp dir> HEAD`, capture with `proof add before --in <tmp dir> --cmd ...`, then `git worktree remove <tmp dir>`. Use the commit before the change in place of `HEAD` if the change is already committed.

3. **Work.** Make the change.
4. **After.** For each claim, capture the same evidence again with `proof add after` and the same `--key`. A before and an after with the same key appear side by side. Done when every key from step 2 has an after.
5. **Gaps.** For each claim the evidence doesn't cover, such as an untested browser or an edge case you didn't run, run `proof unproven "<claim>"`.
6. **Build.** Run `proof build --summary "<what changed, one to three plain lines>"`. It prints the path to PROOF.md. Done when the build succeeds. A refusal lists what's missing.

Tell the person where PROOF.md is. Leave it where `proof build` writes it. Don't copy or move it. To share it, publish it as an Artifact or paste it into the PR body.

When the skill comes from the proof plugin, a Stop hook keeps the turn from ending while a proof is open and not built, and says what's missing. If the work turns out to need no proof, run `proof drop`.
