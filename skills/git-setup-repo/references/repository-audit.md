# Repository Audit And Adoption Plan

Use this reference before changing either a new or existing repository.

## Contents

- Discovery order
- Repository classification
- Gap analysis
- Material decision gate
- Adoption strategy
- Remote repository settings
- Setup brief

## Discovery Order

Read before editing:

1. Root and nearest `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `CONTEXT.md`, and architecture docs.
2. Git state, recent commit grammar, default branch, and existing CI/release workflows.
3. Root manifest, lockfile, workspace config, runtime pin, build orchestrator, and package manifests.
4. Existing lint, format, type-check, test, coverage, and build configs.
5. Hooks, commitlint, staged-file tooling, PR template, and editor workspace.
6. Compose files, migrations, seeders, env examples, provisioning scripts, and deploy scripts.

Useful inventory commands:

```bash
git status --short
git log --format='%h %s' -n 30
rg --files -g 'AGENTS.md' -g 'README.md' -g 'CONTRIBUTING.md' -g 'CONTEXT.md'
rg --files -g 'package.json' -g 'pnpm-workspace.yaml' -g 'yarn.lock' -g 'pnpm-lock.yaml' -g 'package-lock.json' -g 'bun.lock*'
rg --files -g '.github/**' -g '.husky/**' -g '*code-workspace' -g 'compose*.yml' -g 'docker-compose*.yml'
rg -n '"(format|lint|check|test|coverage|build|prepare|provision)"' --glob 'package.json'
```

Use `rg --hidden` where hidden config files are otherwise skipped. Exclude `.git`, dependency directories, build outputs, and generated vendor trees.

## Repository Classification

Classify the repository before choosing templates.

| Dimension | Common values | Consequence |
| --- | --- | --- |
| Maturity | empty/new, established, migration | Copying is safest only for new files; migrations need incremental patches |
| Shape | single package, workspace monorepo, polyglot | Controls scripts, CI jobs, coverage merge, scopes, and subagents |
| Package manager | npm, pnpm, Yarn, Bun | Lockfile, install command, cache action, hook commands, and runtime pins must agree |
| Dependency topology | root-owned, shared config owners, peers, app-local, duplicated | Controls manifests, install layout, singleton frameworks, audits, and package boundaries |
| Build | direct, Vite, framework CLI, task runner | CI and pre-push should call the existing build graph |
| Tests | unit, browser, integration, service-backed | Determines environments, services, provisioning, serialization, and timeouts |
| Deployment | none, package publish, image, serverless, IaC | Add release wiring only when target and rollback are known |

Treat the current shell's runtime and package-manager versions as observations, not project policy. Reconcile the runtime pin, documented support range, manifest engines, resolved dependency engines, CI, containers, and deployment target before changing any of them.

For an established repository, identify why each existing tool is present before replacing it. Search custom rules, ignored files, framework processors, generated artifacts, and package-specific commands. A migration from ESLint/Prettier/Jest is not complete until equivalent important behavior is preserved or consciously dropped.

## Gap Analysis

Create a compact ledger before implementation:

```text
Repository setup brief
- Shape: <single package / monorepo / polyglot>
- Runtime: <version source>
- Package manager: <manager, version, lockfile>
- Runtime boundaries: <client, server, worker, library, and their test/coverage status>
- Dependency topology: <root/config/runtime/app owners, peer contracts, duplicate declarations and resolved copies>
- Local services: <service, version, dev/test purpose>
- Quality commands: <format, lint/check, test, coverage, build>
- Hooks: <current and proposed>
- CI: <events, required job, cache, services>
- Docs/workspace: <present, missing, stale>
- Release/deploy: <known flow or deferred>

Decisions needed
- <material choices not already explicit in the user request>

Workflow recommendation
- <continue directly / continue in Plan mode before implementation>
```

Mark each feature as:

- `keep`: current behavior is healthy and consistent;
- `adapt`: keep ownership but align commands/config;
- `add`: capability is absent;
- `migrate`: tool replacement is explicitly in scope;
- `defer`: requirements or authority are missing.

Do not turn every optional repository feature into required scope. A public library may need licensing, release, and security docs; a private application may not. A database-free package does not need Compose or provisioning.

## Material Decision Gate

Complete read-only discovery first. Editing may begin only after material choices are already explicit, user-approved, or intentionally deferred.

| Area | Confirm before editing | Safe autonomous work |
| --- | --- | --- |
| Repository shape | Monorepo conversion; split, merge, move, or new shared/config packages | Inventory the graph and recommend a target |
| Dependency ownership | Relocate shared dependencies; introduce peers; change peer ranges or public consumer contracts | Find duplicates and prepare an owner map |
| Runtime/upgrades | Node/package-manager support changes; framework, bundler, lint, or test major upgrades | Preserve pins; add compatible versions for approved new tooling |
| Tests/CI | E2E/browser infrastructure; CI coverage, thresholds, artifacts, audits, required checks, or material runtime cost | Add focused local tests inside the agreed scope |
| Services | Add/remove databases, caches, emulators; choose image majors or destructive seed/reset behavior | Mirror an already approved service contract |
| Release/deploy | Provider, environment, trigger, secrets, component boundaries, migrations, rollback | Audit evidence and draft a recommendation |
| Tool migration | Replace linter/formatter/test runner or create repository-wide mechanical churn | Preserve style and format directly changed files |
| Remote settings | Mutate branch protection, environments, secrets, visibility, labels, merge policy, ownership, or public policy files | Read-only audit and document required host setup |

Do not re-ask an explicit user choice. Ask at most three grouped questions, each with a recommendation and concrete trade-off. For a monorepo conversion, broad migration, or multiple coupled decisions, print `Workflow recommendation: continue in Plan mode before implementation` before the questions. Avoid a questionnaire for routine paths, config syntax, or cleanup inside an agreed design.

## Adoption Strategy

### New repository

Start with the smallest coherent vertical setup:

1. runtime/package manager and lockfile;
2. format, lint/type-check, test, coverage, and build scripts;
3. hooks and commit rules;
4. services/provisioning if tests or development require them;
5. CI calling those scripts;
6. README and workspace map;
7. release/deploy only when the artifact lifecycle exists.

### Existing repository

Prefer an incremental sequence:

1. Make current commands deterministic and document the baseline.
2. Resolve material decisions before editing.
3. Preserve runtime and application-toolchain compatibility unless their migration is explicitly part of setup.
4. Add new configs alongside old tooling if comparison is needed.
5. Run both on representative source, tests, generated files, and framework files.
6. Resolve meaningful rule differences; do not chase formatter-only diff noise early.
7. Switch package scripts and hooks.
8. Switch CI.
9. Remove old dependencies/config only after no caller remains.
10. Keep tool-migration changes separate from product behavior where possible.

Never overwrite user edits or broad-stage generated churn. If setup generates files, identify their source command and decide whether they are committed artifacts before proceeding.

## Remote Repository Settings

Files alone do not finish repository setup. Audit, but do not mutate without authorization:

- default branch and branch deletion policy;
- required checks and merge queue compatibility;
- pull request review requirements;
- force-push and deletion protections;
- labels referenced by workflows;
- GitHub Environments, secrets, variables, and deployment protection rules;
- package/container permissions;
- repository visibility, license, vulnerability reporting, and security policy;
- CODEOWNERS and team/reviewer ownership.

Do not add a workflow that references a label, environment, secret, app, or reviewer that does not exist without documenting the required host-side setup.

## Setup Brief Acceptance

Before broad implementation, make sure the brief answers:

- Which commands are the local source of truth?
- Which files will be copied, patched, or left alone?
- Which package owns each shared dependency family, and which duplicate versions remain justified?
- Which services are required for development versus tests?
- Which checks block commits, pushes, and pull requests?
- What coverage surface is meaningful?
- Does every runtime boundary have an honest automated-test and coverage decision?
- What repository-host changes remain manual?
- Which release/deploy choices are evidenced and approved, or why is automation deferred?

Confirm every unresolved material answer with the user before editing that area. Explicit choices in the request count as confirmation.
