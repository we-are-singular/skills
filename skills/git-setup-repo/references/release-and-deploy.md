# Release And Deployment

Use this reference only when the repository already makes the release target and deployment contract discoverable.

## Contents

- Evidence gate
- Preferred flow
- Exact revision safety
- Release shapes
- Permissions and environments
- Migrations, rollback, and validation

## Evidence Gate

Do not invent deployment automation from a framework or hosting dependency alone. Require evidence for:

- the artifact: package, static bundle, server bundle, container, infrastructure program, or multiple components;
- the checked-in build/publish/deploy command;
- target environments and provider/project identifiers;
- required secrets/variables and who owns them;
- migration and generated-infrastructure order;
- trigger policy: default-branch merge, tag, stable release, path change, or manual dispatch;
- rollback or safe retry behavior;
- whether components deploy together or independently.

Present unresolved provider, environment, trigger, secret, component-boundary, migration, and rollback choices to the user before editing. Wire release/deploy only after the material choices are explicit and approved; if they remain unanswered, stop at CI and document release/deploy as deferred.

## Preferred Flow

Keep verification and deployment coupled to the exact tested revision:

```text
pull request / merge group
  -> required Lint, Test and Build
  -> default-branch revision
  -> development/staging release, if policy allows
  -> stable tagged/GitHub release
  -> protected production deployment
```

Useful general policies:

- Default-branch merges may deploy a development environment after CI succeeds.
- Production deploys from a published, non-prerelease release or another explicit immutable promotion event.
- GitHub Environments own environment-specific secrets, protection rules, and deployment history.
- The deploy command receives an exact Git SHA, image digest, or package version.
- Production concurrency queues and serializes; it should not cancel a running deployment for a newer commit.
- Reusable workflows centralize repeated build/publish logic, with minimal explicit inputs and secret inheritance only when appropriate.

Do not trigger a live deployment while merely setting up repository files.

## Exact Revision Safety

The deployed commit must be the commit that passed CI.

- A reusable workflow called directly from successful default-branch CI naturally retains the caller revision; still pass/report it explicitly.
- A tag/release workflow should resolve the tag to its immutable commit and check out that ref.
- A `workflow_run` workflow must explicitly use `github.event.workflow_run.head_sha`; the event's default `GITHUB_SHA`/ref can refer to the default-branch head instead of the triggering revision.
- Container promotion should prefer a digest over rebuilding a mutable branch.
- Report the deployed SHA/version in logs and deployment metadata.

Never check out an untrusted pull-request head in a privileged `workflow_run` context with secrets. Read current GitHub security guidance for that event before using it.

## Release Shapes

### Published package

Verify package metadata, files allowlist, build output, dependency/peer contracts, versioning policy, registry auth, provenance/signing policy, and whether releases are independent in a monorepo. If releases derive bumps or changelogs from commit types, ensure the accepted `feature` alias maps to the same behavior as conventional `feat`. Pack the package, inspect the tarball, and install/import it in a clean external consumer before wiring publish; a workspace-only dry-run can miss hoisting and symlink failures.

### Container image

Use a reusable workflow with least privilege, a pinned builder/metadata action, registry login, deterministic tags, digest output, and cache appropriate to the builder. Build once where possible; promote the digest rather than rebuilding for production.

### Hosted application or worker

Prefer a checked-in deploy script or package command that both humans and CI call. Pass environment and exact revision explicitly. Keep provider CLI versions repository-owned or pinned.

### Infrastructure as code

Keep preview and apply separate. Preview on pull requests only with safe credentials and policy; apply after protected promotion. Regenerate derived infrastructure files and fail if committed generated output drifts. Require a reviewable plan for destructive changes.

### Multiple components

Start with full release unless independent components, dependency order, shared-path invalidation, and rollback are proven. Selective release scripts often miss config, schema, shared package, or generated inputs. If selective deployment is needed, test the change detector and maintain its shared-path rules as production code.

## Permissions, Secrets, And Environments

Declare permissions explicitly. Common examples:

- `contents: read` for checkout;
- `packages: write` only for registry publication;
- `id-token: write` only for configured OIDC federation;
- deployment/environment access only where required.

Prefer short-lived OIDC credentials over long-lived provider tokens when the provider supports it and the repository is ready to configure trust. Never add placeholder secrets that look real. Document every required secret/variable and the environment/repository/org level that owns it.

Use environment protection for production approvals when required. Confirm that reusable workflows and forks receive only the permissions and secrets intended.

## Migrations And Rollback

Define order explicitly:

1. backward-compatible schema/infrastructure changes;
2. application deployment;
3. data backfill or destructive cleanup after compatibility is proven.

If the existing platform requires a different order, document why and how rollback works. A deploy workflow is incomplete if a failed migration leaves the application in an unknown state with no retry/repair path.

## Validation

Before enabling triggers:

- run build/package/deploy dry-run commands locally or in a nonproduction environment;
- validate reusable workflow inputs, outputs, secrets, and permissions;
- verify checkout/ref handling with an exact SHA;
- verify generated files and change detection;
- verify environment serialization/concurrency;
- verify artifact/package contents and version/tag mapping;
- document manual approval, rollback, and required host-side configuration.

If the deploy provider cannot be exercised safely during setup, leave the workflow manual or draft and report the unverified boundary rather than claiming completion.
