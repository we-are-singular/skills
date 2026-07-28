# CI And Service Provisioning

Use this reference to build `.github/workflows/ci.yml`, optional service containers, Compose-based local infrastructure, and `script/provision.sh`.

## Contents

- Baseline CI contract
- Events, permissions, and concurrency
- Checkout, runtime, install, and cache
- Lint, test, coverage, and build
- CI services
- Local provisioning
- Workflow validation and pitfalls

## Baseline CI Contract

Create one required job with the stable id `lint-test-build` and display name `Lint, Test and Build`. A new or small repository should run the full contract on every pull request, merge group, and push to the default branch:

1. check out the intended revision;
2. set up the pinned runtime and package manager cache;
3. install from the lockfile;
4. audit dependencies if repository policy requires it;
5. provision only CI-owned data/schema prerequisites;
6. run format check and lint/type/framework checks;
7. run deterministic tests;
8. run coverage if it is a required CI contract;
9. build real deployable/library outputs;
10. verify committed generated or build-time files did not drift when the repository owns such outputs.

Start with `assets/templates/.github/workflows/ci.yml` for npm or `ci-pnpm.yml` for pnpm. When tests actually require PostgreSQL or Redis, use the matching `ci-with-services.yml` or `ci-pnpm-with-services.yml` variant and remove either unused service.

## Events, Permissions, And Concurrency

Typical validation events:

```yaml
on:
  push:
    branches: [__DEFAULT_BRANCH__]
  pull_request:
    types: [opened, synchronize, reopened]
  merge_group:
  workflow_dispatch:
```

Keep `merge_group` when the repository uses or may use a merge queue. Add path filters only after proving they cannot skip a required check or deploy-relevant change.

Declare least privilege:

```yaml
permissions:
  contents: read
```

Add `pull-requests: read`, `packages: write`, `id-token: write`, deployments, or other scopes only for a step that requires them. Once any permission is declared, unspecified permissions become unavailable; audit reusable workflows too.

Choose one concurrency policy:

- Validation-only CI: group by workflow plus PR/ref and use `cancel-in-progress: true` so stale revisions stop.
- Release-coupled default-branch CI: queue the default-branch group with `queue: max` so every merge is processed, while non-default revisions use unique groups or a separate workflow.
- Production/release workflows: serialize by environment or component and queue rather than cancel.

Current GitHub Actions supports `queue: max`, but it cannot be combined with `cancel-in-progress: true` in the same concurrency block. Verify current [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) while applying this skill.

## Checkout, Runtime, Install, And Cache

Use current official major versions or immutable SHAs according to repository policy. The bundled actions are examples and must be checked when copied. Verify releases from each action's official repository or Marketplace page, not a setup snippet in another project's documentation. For example:

```bash
gh api repos/actions/checkout/releases/latest --jq .tag_name
gh api repos/actions/setup-node/releases/latest --jq .tag_name
gh api repos/actions/upload-artifact/releases/latest --jq .tag_name
```

Compare the result with both the asset and the final workflow. Do not downgrade an asset from a verified current major because a documentation example still shows an older one. When pinning an immutable SHA, retain the release tag in a comment for maintainability.

Use `fetch-depth: 0` only when affected-task filtering, changelog/release logic, or diff checks need history. Otherwise the default shallow checkout is faster.

Use runtime caching through the official setup action:

```yaml
- uses: actions/setup-node@<current-major>
  with:
    node-version-file: .nvmrc
    cache: npm
    cache-dependency-path: package-lock.json
```

The `packageManager` field may let setup-node detect npm for caching, but setup-node does not install the npm version named there. If the repository requires an exact npm version rather than the version bundled with the pinned Node release, install that pinned npm version and assert `npm --version` before the frozen install. Reproduce that sequence locally with the pinned Node version; success under a newer host npm does not prove CI. Do not claim an exact npm baseline in the README unless CI enforces or inherits that exact version deliberately.

Set up pnpm before setup-node requests a pnpm cache. When root `package.json#packageManager` declares pnpm and its version, let `pnpm/action-setup` read that single authority; omit the action's `version` input so two declarations cannot conflict. Specify the action input only when the repository deliberately has no `packageManager` field. For workspaces with multiple lockfiles, list the authoritative dependency paths explicitly.

An application normally validates the one Node line used by its build and deployment. A published library that declares support for several Node release lines should test its public contract across that supported matrix, while keeping packaging/publication in one explicitly chosen job. Do not advertise a broad `engines.node` range that CI never exercises.

Do not cache `node_modules`. Cache package-manager downloads plus expensive reproducible task/build caches such as `.turbo` only when the key includes OS, relevant lockfiles/config, and a useful branch/base fallback. Treat build output caching separately from dependency caching.

Install with the frozen command from `references/javascript-quality.md`. Do not run an unpinned global task runner in CI when the repository owns it locally.

Dependency auditing is policy-sensitive. If enabled, decide whether dev dependencies count, what severity fails, and whether the package manager's audit endpoint is reliable enough to be required. Keep it a named step rather than hiding it inside lint.

After that policy is approved, add the manager-appropriate command as its own step:

```yaml
- name: Check for high-severity vulnerabilities
  run: <manager> audit --audit-level=high
```

## Lint, Test, Coverage, And Build

Prefer explicit named steps that call root scripts:

```yaml
- name: Check formatting
  run: npm run format:check
- name: Lint and type-check
  run: npm run lint
- name: Test
  run: npm run test
- name: Build
  run: npm run build
```

This makes failures readable and keeps local/CI behavior aligned. If `lint` does not include type/framework checks, add a separate `check` step.

Affected-task optimization is not the initial default. Enable it only when:

- the workspace dependency graph is accurate;
- checkout history is sufficient;
- shared/config/generated paths invalidate the right packages;
- default-branch runs remain full;
- a change cannot skip a required check by falling outside a maintained glob.

Coverage policy must be explicit:

- report only and upload an artifact;
- publish to an external coverage service;
- enforce agreed thresholds;
- run outside the required fast CI job.

When no repository policy already answers this, treat coverage placement, thresholds, artifacts, external publication, and whether coverage blocks pull requests as material user decisions. Recommend a default with its CI-time and maintenance cost before editing the workflow.

Do not claim coverage merely because a Vitest config contains a `coverage` block. Invoke the coverage command and confirm all intended packages/languages contribute. Upload only useful report formats and use current artifact action guidance.

After coverage placement and artifact retention are approved, replace the ordinary test step or add a separate non-blocking job deliberately:

```yaml
- name: Test with coverage
  run: <manager> run test:coverage

- name: Upload coverage report
  uses: actions/upload-artifact@<current-major>
  with:
    name: coverage-${{ github.sha }}
    path: coverage
    if-no-files-found: error
    retention-days: 7
```

Keep the baseline templates on deterministic `test`; their lack of an artifact is intentional until this material choice is resolved.

After generation/build steps, consider a dirty-tree guard when the repository commits generated files:

```bash
if [ -n "$(git status --porcelain)" ]; then
  git status --short
  echo "Generated files changed; regenerate and commit them." >&2
  exit 1
fi
```

Run this only after understanding which tools legitimately write during CI. It should catch drift, not formatter mutation that CI should never perform.

## CI Services

Introducing or removing CI infrastructure is a material decision even when a test could use it. Once the service-backed test scope is approved, add a service only when a test or migration connects to it. For every service:

- pin an image major/version compatible with development and production;
- use deterministic non-secret CI credentials;
- set a real health check and bounded retries;
- expose only required ports;
- use the service hostname from other service containers and localhost from runner steps;
- put runner connection URLs in job `env` without copying production secrets;
- migrate/bootstrap after health, before tests.

### PostgreSQL

Use a disposable database, explicit user/password/database, `pg_isready`, and optionally tmpfs for CI speed. Match the application's actual PostgreSQL major. Use a stable container name only if later steps deliberately call `docker exec`.

Derive persistent-volume and tmpfs targets from that selected image. The official image uses `/var/lib/postgresql/data` through PostgreSQL 17 and changed the recommended mount to `/var/lib/postgresql` for PostgreSQL 18 and later. Resolve `__POSTGRES_DATA_MOUNT__` from the current official image documentation instead of retaining an older hardcoded target.

Do not add generic durability tuning. If migration-heavy CI needs it, document that the database is disposable, run explicit `ALTER SYSTEM` commands, and keep the optimization confined to CI.

### Redis

Use a pinned Redis image and a `redis-cli ping` health check. Do not use `latest`. Remove Redis from the template if no test connects to it.

### Dependent services and emulators

For search engines, queues, cloud emulators, ledgers, or other providers:

- pin the exact tested image;
- inspect whether the image contains the health-check client;
- model dependencies through service hostnames;
- expose only the runner-facing API;
- wait for actual readiness rather than assuming dependency installation was slow enough;
- keep provider-specific configuration out of the generic CI template.

## Local Provisioning

Local Compose and CI services solve different problems. Do not call the full local `script/provision.sh` from CI when it starts its own containers; CI should use Actions services and run only schema/bootstrap commands.

For local setup, adapt the bundled `ops/docker-compose.yml` and `script/provision.sh`:

- use one named Compose project to avoid collisions;
- start foundational databases before dependent services;
- include persistent development storage and, when useful, a separate disposable test database;
- check required CLIs early;
- retry only readiness-sensitive commands;
- keep migration errors visible;
- create secondary databases/buckets/ledgers idempotently;
- migrate development and test stores explicitly;
- support `up` and `down` when a lifecycle command helps contributors;
- print useful URLs and the next command without leaking credentials.

For POSIX `sh`, use `set -eu` and POSIX syntax. If arrays, process substitution, or other Bash features are needed, use `#!/usr/bin/env bash` and `set -euo pipefail`. Never declare `/bin/sh` and use Bash-only brace expansion.

## Workflow Validation And Pitfalls

Validate:

```bash
docker compose -f ops/docker-compose.yml config
sh -n script/provision.sh
<manager> run format:check
<manager> run lint
<manager> run test
<manager> run build
```

Use `shellcheck`, `actionlint`, or an equivalent local checker when available. Do not install an unapproved global tool just to satisfy a checklist.

Avoid these failure modes:

- a job named lint/test/build that never runs a full lint on the default branch;
- service containers without effective health checks;
- floating image tags;
- hidden migration output inside retry loops;
- `NODE_ENV=CI` copied into a framework that expects `test` or `production` semantics;
- secrets exposed to forked pull requests;
- generated-file checks after commands that intentionally write formatting changes;
- affected filters that miss shared config or deploy inputs;
- release/deploy triggered from a generic `workflow_run` checkout that does not pin `github.event.workflow_run.head_sha`;
- deploy steps using the default branch head instead of the exact commit that passed CI.

When CI directly calls a reusable release workflow after the required job, the tested revision is easier to preserve. When using `workflow_run`, explicitly check out and report the triggering run's head SHA and apply the event's security restrictions.
