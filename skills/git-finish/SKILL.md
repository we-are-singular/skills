---
name: git-finish
description: Carry an assigned task, branch, PR, or stack through implementation, local review, publication, CI, and review fixes until ready to merge. Use when the user asks to finish the work through PR readiness, or a parent agent delegates that outcome. Merge only with explicit authorization.
---

# Git Finish

Own the work until the PR is ready to merge. Finish the implementation, satisfy its definition of done, review it locally, publish it, and keep working through CI and reviewer feedback. A pushed branch, an open PR, or a pending review is an intermediate state.

Compose the existing skills rather than replacing their mechanics:

- `singular-code-review` for local review and evidence-backed findings.
- `git-commit-pr` for commit boundaries, staging, validation, and PR preparation.
- `git-fix-pr` for blocker triage, reviewer replies, thread resolution, and batched follow-up pushes.
- `gh-stack` when managing dependent branches and PRs.

Read each skill before its phase. Resolve it from the available skill catalog, sibling skill directories, or the repository that supplies it. If a required skill is missing, identify the missing dependency and the phase it prevents; do not silently substitute a partial workflow.

## Establish Scope And Authority

Recover the original request, conversation decisions, applicable repository instructions, local `TODO.md` / `PLAN.md`, linked specifications or tickets, and any existing PR discussion. Establish the repository, worktree, branch, intended base, owned changes, and existing PR or stack before editing or publishing. Resume existing work instead of creating duplicate PRs.

Explicit user invocation of this skill requests the complete lifecycle for the assigned work: implementation, review fixes, commits, pushes, PR creation or updates, marking ready, and reviewer replies/resolution. An explicitly delegated invocation inherits only the authority and scope the parent actually received and passed on. Carry that authorization into the component skills: their routine planning and publish confirmations are already answered for this work. Show concise decisions and progress, then proceed.

Automatic skill selection alone supplies no publication or merge permission. Check the actual user request and inherited authorization. Respect narrower instructions such as local-only work, draft-only publication, a named worktree, or a limit on which PRs may change. Merge and enabling auto-merge require explicit authorization covering the relevant PRs; readiness alone does not authorize either. Production operations require their own authorization.

Resolve routine implementation choices and clear review fixes from repository evidence. Ask only for a material product or architecture decision, conflicting instructions, unclear ownership, missing authority, or an external blocker that cannot be resolved within scope. Complete independent work while that decision is pending. A delegated worker escalates to its parent before interrupting the user.

## Set The Completion Goal

Use the host's persistent goal facility when available and authorized, with an objective tied to the actual task and its PRs: finish the agreed requirements and leave every owned PR reviewed, green, resolved, and ready to merge; include merging only when authorized. Reuse an active goal that already covers this work. Preserve its full scope and budget; a worker must not complete its parent's broader goal.

For substantial work, maintain the existing local scratchpad or an untracked `TODO.md`. Record acceptance criteria, remaining work, branch/PR ownership, dependencies, authorization limits, and current CI/review evidence with commit IDs. Keep this scratchpad out of commits unless it is an intended deliverable. Refresh live Git and GitHub state when resuming after a context boundary.

## Coordinate Delegated Work And Stacks

Apply this section when work is delegated or spans dependent PRs. The same completion audit applies to each owned PR and the integrated result.

### Ownership And Worker Completion

When delegation is permitted, assign each worker a bounded deliverable, definition of done, repository/worktree, branch or PR, dependency base, relevant decisions, and authorization limits. State who owns publication, ready promotion, reviewer replies, and merge. A worker may invoke `git-finish` for its slice or subtree, including coordinating descendants when permitted, within the inherited authority.

Give each branch and mutable stack metadata one writer; use separate worktrees for concurrent branch work. Workers must not switch another agent's checkout or rewrite its branch. Independent PRs can finish concurrently. For a shared stack, one coordinator owns restacking, pushes that rewrite multiple branches, and promotion order; workers publish only under that arrangement.

A worker returns its branch/worktree, PR URL, verified head and base, completed acceptance criteria, validation and review evidence, and remaining dependencies or blockers. If authority prevents an external step, return the concrete prepared result to the parent and label its actual state, such as locally reviewed or draft published. The coordinator verifies current remote state and shared contracts after integration before completing the overarching goal.

Keep responsibility for workers until their assigned outcomes are verified. Before resuming an apparently stopped worker, inspect its latest actions, live task or writer status, pending approvals, and explicit pauses or cancellations. Missing connectivity or a not-loaded UI does not prove that it stopped. Resume unfinished, unpaused work within existing authority or explicitly transfer ownership, preserving one writer per branch.

### Stack Boundaries And Tracking

Load `gh-stack` before operating a stack. Keep independent work separate and use a linear stack for dependent, independently reviewable layers. Preserve an existing coherent stack. If stacked PRs are unavailable, use repository-supported dependent branches/PRs that preserve the same diff and review boundaries; otherwise report the limitation.

For large work owned by one agent, keep one overarching goal and scratchpad across the layers. Implement and locally review each coherent layer on its owning branch before building the next. Task size alone does not require delegation.

Track layer order, owner, branch, PR URL, parent branch, verified head and dependency commits, and implementation/CI/review state in the scratchpad. Select the actual owning PR for each `git-fix-pr` invocation; the checked-out top branch is not automatically the fix target.

### Publish Together, Review In Order

1. Finish, locally review, validate, and commit each layer through the workflow below. Review its diff against its own parent.
2. Push all owned branches and publish their draft PRs with correct bases and dependency links. Inspect CI trigger filters; workflows restricted to trunk may omit checks on upper layers.
3. Mark the lowest unfinished layer ready, then follow CI, review, and fixes until it passes the completion audit against its intended base.
4. Promote the next layer and repeat. A green parent can stay open while its child is reviewed. Advance only one draft into its review loop at a time; preserve already-ready PRs and resume with the lowest affected unfinished layer.
5. Reinspect the whole stack before reporting readiness in landing order. Corrections and restacks can invalidate earlier evidence. Independent stacks may progress concurrently under separate owners.

### Corrections And Parent Merges

Fix the layer that owns the behavior, even when an upper PR's review discovered the problem. Validate and commit there, then restack descendants, resolve conflicts, inspect their diffs, and publish affected branches together after the fix pass. Rebase before preparing replies that cite commits. Coordinate rewrites with the owner, preserve others' commits, and use the stack tool's safe update mechanism or lease-protected pushes.

After a parent changes, recheck affected descendants' contracts, CI, and reviews against the resulting heads and bases. If a parent merges, synchronize the stack and verify remaining PRs target the intended surviving parent or trunk. Account for squash merges, inspect for duplicated or lost changes, and validate conflict resolutions before obtaining fresh remote evidence.

Stack readiness means its layers can land in dependency order. If a required check or branch protection genuinely depends on a parent merging first, report that precise gate instead of claiming the whole stack is ready. For authorized merges, inspect which PRs the operation includes: some stack commands include all unmerged ancestors. Every included PR needs authorization and a passing audit; confirm merge receipts and reconcile descendants before proceeding.

## 1. Finish The Agreed Work

Turn the task's definition of done into concrete requirements with evidence for each one. Complete outstanding implementation, tests, documentation, wiring, and required verification. Reconcile task-related TODOs and plan items against the actual result; remove an item only when completed or demonstrably obsolete. Keep unrelated and explicitly deferred work separate.

Match verification to the changed behavior and repository requirements. Reuse relevant checks already passed for the current files; run fresh checks when changes invalidate them. Preserve unrelated user changes and curated staging.

**Exit:** every in-scope requirement has completion evidence. Keep a blocked requirement open while progressing independent work. Implementation that merely passes the available tests is insufficient when the original requirements remain incomplete.

## 2. Review Locally And Fix

Invoke `singular-code-review` against the intended PR diff, including the relevant surrounding code and intent. This invocation includes authorization to fix findings within the assigned scope. Use that skill's independent review lanes when delegation is available under the host's rules; sequential review remains valid when it is not.

Fix substantive findings and validate the affected behavior. Push back on findings contradicted by code, requirements, or established ownership, recording the evidence. Optional nits need not expand the work. Deferring a real blocker requires an authorized scope decision. Review consequential corrections again until no substantive finding remains unaddressed.

**Exit:** the final local diff satisfies the requirements, has been reviewed, and has no unresolved substantive local findings.

## 3. Commit, Publish, And Mark Ready

Invoke `git-commit-pr` with the authorization established above. Prepare focused commits, run applicable checks, inspect the final diff, and write a PR title/body that describes the resulting behavior. Use the actual intended base; a stacked layer targets its parent rather than trunk. Keep temporary plans and artifacts out of the commit set.

Before pushing, inspect upstream and push settings and specify each branch's source and remote destination explicitly. For the checked-out feature branch, use a refspec such as `HEAD:refs/heads/<feature-branch>`; this avoids inheriting a trunk destination from worktree configuration. Wait for a successful push and confirm that remote branch exists before creating or updating the PR.

Publish the branch and create or update its PR. Keep the body aligned with the final scope, known ticket relationship, useful behavioral verification, and dependency links. Mark the PR ready for review when its local work is complete. Read back the remote head, base, draft status, and CI/review activity; sending the command is not proof that it succeeded.

For a stack, follow the publication sequence above. Preserve existing ready PRs when resuming; use the repository's reviewer trigger instead of toggling draft status to manufacture another review.

**Exit:** the correct PR is published and ready, and CI plus the expected review have started or have a concrete trigger problem to investigate.

## 4. Follow CI And Review To Convergence

Poll GitHub approximately every 60–120 seconds. CI and automated review commonly take about five minutes; this is an expectation, not a timeout. Use interruptible waits and respect the host's wait limits without increasing GitHub polling frequency. Continue independent work while waiting, and keep the user informed of meaningful state changes.

At each poll, inspect the current head, base, mergeability, checks, review submissions, PR-level comments, and inline threads, including pagination where required. Route new conflicts or changed stack dependencies into the fix loop promptly. Verify evidence against the current head and intended base. An automated review may deliver LGTM as a comment rather than a formal approval; still satisfy any separately required approvals. A passing review job without a positive verdict, an old LGTM, or an empty unresolved-thread list does not prove approval.

For failures, requested changes, unresolved comments, body TODOs, or merge conflicts, invoke `git-fix-pr` with the exact PR and standing authorization to handle in-scope blockers. Keep an evidence-backed disposition for each item. Accept valid fixes, explain justified pushback, and ask only when a material decision exceeds the agreed scope. New routine blockers remain covered by the same authorization.

Finish each fix pass before pushing: implement, validate, commit, perform any necessary rebase, update the PR body, and post concise reviewer replies and resolve handled threads. If replies require remotely available commits, prepare their exact text first, push once, then post them immediately. Follow the component skill's batching discipline to avoid triggering reviews for unfinished fixes.

After every push, rebase, restack, or base change, verify CI and review again for every affected PR. Resolve threads only when their issue is actually fixed or supported pushback has addressed it; an unresolved substantive concern remains a blocker. Reinspect repeated failures before retrying; use reruns only for diagnosed transient failures. Preserve required checks and review gates.

If review does not start, inspect the actual trigger, workflow, or reviewer service and use its supported retry path. Missing checks, unknown merge state, and unavailable review evidence need investigation. Keep pending work active while it is progressing. Surface a genuine permissions, service, or human-decision blocker with its evidence and required next action instead of claiming readiness.

**Exit:** fresh remote evidence satisfies the completion audit below. Repeat this phase as often as necessary; a follow-up push does not finish the task.

## 5. Audit And Finish

Read back the final state immediately before declaring completion. Confirm merge receipts for owned PRs that have already landed. For each remaining owned PR, prove:

- The original definition of done is satisfied; task-related plan items and PR-body TODOs are complete or explicitly accepted as out of scope.
- All intended changes are committed and pushed, and the local branch tip agrees with the remote PR head. Any remaining local changes are accounted for.
- The PR is open and ready for review, with the correct base and an accurate title/body.
- Required CI and task-relevant checks pass for the current revision; skipped or missing checks count only when demonstrably inapplicable.
- The latest applicable review is LGTM or approved for the current revision, required approvals are satisfied, no outstanding change request remains, and all review threads are resolved with evidence-backed dispositions.
- GitHub reports no conflicts or unexplained merge blocker. Stack dependencies are explicit and the stack is ready to land in dependency order.

If merge is authorized, merge only the covered PRs in dependency order using the repository's workflow. Confirm actual merged state; a queued merge or successful merge command is not a merge receipt. After a parent lands, recheck any affected descendants before merging them. Verify deployment only when it belongs to the authorized definition of done.

For partial merge authorization, completion combines confirmed merges for the covered PRs with verified readiness of the remaining owned PRs.

Complete a persistent goal only when its whole objective is proven, following the host's goal-status rules. Otherwise leave the remaining work explicit and continue whenever progress is possible.

Report the PR links, ready-to-merge or confirmed merged state, relevant validation, and any genuine remaining limitation. For a stack, include landing order. When merge was not authorized, finish with the PRs ready and leave them open; no additional merge-permission question is needed.
