# __PROJECT_NAME__

__ONE_PARAGRAPH_PROJECT_DEFINITION__

<!-- TODO(git-setup-repo): keep this pointer only when the docs index exists. -->
Read [`docs/README.md`](docs/README.md) for __DEEPER_CONTEXT__. This README is the operational codebase map: setup, commands, structure, and repository rules.

## Project decisions

- **Runtime:** __RUNTIME_AND_VERSION_POLICY__
- **Application boundary:** __PRIMARY_APP_OR_LIBRARY_BOUNDARY__
- **Persistence:** __DATABASE_OR_STATE_OWNERSHIP__
- **Testing:** __TEST_LEVELS_AND_SERVICE_REQUIREMENTS__
- **Deployment:** __ARTIFACT_AND_ENVIRONMENT_POLICY__

## Prerequisites

| Tool | Version source | Purpose |
| --- | --- | --- |
| Node.js | `.nvmrc` and `package.json#engines` | Runtime and repository tooling |
| __PACKAGE_MANAGER__ | `package.json#packageManager` | Dependencies and scripts |
| Docker | __MINIMUM_OR_SUPPORTED_VERSION__ | Local services |
| __EXTERNAL_CLI__ | __VERSION_SOURCE__ | __PURPOSE__ |

Remove tools that are not required for the normal contributor path.

## Quick start

```bash
__INSTALL_COMMAND__
__PACKAGE_MANAGER__ run provision  # Remove when no local services are required
__PACKAGE_MANAGER__ run dev
```

Useful local endpoints:

- Application: __LOCAL_APP_URL__
- Service health: __LOCAL_HEALTH_URL__
- Database UI: __LOCAL_DATABASE_UI_URL__

## Commands

Run these from the repository root unless noted.

```bash
# Development
__PACKAGE_MANAGER__ run provision       # Start local/test services and apply migrations
__PACKAGE_MANAGER__ run dev             # Start the development graph
__PACKAGE_MANAGER__ run build           # Build deployable/package output

# Verification
__PACKAGE_MANAGER__ run format          # Write Oxfmt-supported files
__PACKAGE_MANAGER__ run format:check    # Verify formatting without writing
__PACKAGE_MANAGER__ run lint            # Type/framework checks plus Oxlint
__PACKAGE_MANAGER__ run test            # Deterministic tests without coverage
__PACKAGE_MANAGER__ run test:watch      # Local watch mode
__PACKAGE_MANAGER__ run test:coverage   # Full coverage report

# Repository workflow
__PACKAGE_MANAGER__ run commit          # Remove if no interactive helper exists
```

### Workspace examples

```bash
__WORKSPACE_DEV_EXAMPLE__
__WORKSPACE_TEST_EXAMPLE__
__WORKSPACE_LINT_EXAMPLE__
```

Remove this subsection for a single-package repository.

## Seed or sample data

__STATE_WHETHER_PROVISIONING_SEEDS_DATA__

```bash
__SAFE_IDEMPOTENT_SEED_COMMAND__
```

Document destructive behavior, the target database/environment, idempotency, and required follow-up commands. Remove this section when no seed workflow exists.

## Structure

```text
apps/
  __APP__/          # __APP_OWNERSHIP__

packages/
  __PACKAGE__/      # __PACKAGE_OWNERSHIP__

config/             # Shared compiler, build, test, or framework configuration
docs/               # Product/domain context, ADRs, specs, and reading order
ops/                # Local/deployment infrastructure and provider configuration
script/             # Provisioning and repository automation
```

Replace this tree with the real repository. Do not retain empty conventional folders.

## Architecture boundaries

### `__PRIMARY_APP_PATH__`

__PRIMARY_APP_RESPONSIBILITIES_AND_NON_GOALS__

### Shared packages

- `__CONTRACT_PACKAGE__` owns __SCHEMAS_DTOS_OR_EXTERNAL_CONTRACTS__.
- `__DATABASE_PACKAGE__` owns __CLIENT_REPOSITORIES_MIGRATIONS_AND_SEEDS__.
- `__UI_PACKAGE__` owns __SHARED_UI_PRIMITIVES_AND_STYLES__.
- `__UTILS_PACKAGE__` owns __GENUINELY_SHARED_RUNTIME_HELPERS__.

Explain package ownership only when these boundaries exist. Prefer facts and prohibitions that prevent common misplacement.

### Dependency ownership

- Root owns __APP_AGNOSTIC_REPOSITORY_TOOLING__.
- `__TYPESCRIPT_CONFIG_PACKAGE__` owns __COMPILER_PRESETS_AND_GLOBAL_TYPES__.
- `__VITE_CONFIG_PACKAGE__` owns __VITE_VITEST_COVERAGE_AND_SHARED_PLUGINS__.
- `__SINGLETON_HOST_PACKAGE__` provides __SINGLETON_RUNTIME__, with reusable consumers declaring compatible peers.
- App packages retain internal workspace packages, concrete singleton/peer providers they host, and __APP_ONLY_DEPENDENCIES__.

Document justified duplicate versions and public-package exceptions. Remove this section for a single-package repository.

## Environment files

| File | Committed | Purpose |
| --- | --- | --- |
| `.env` | only when values are safe defaults | Shared development defaults |
| `.env.test` | yes, with safe deterministic values | Test-only defaults |
| `.env.local` | no | Machine overrides and local secrets |
| `.env.example` | yes when needed | Required keys without secret values |

Rules:

- Real process environment values win.
- Tests do not read developer-local overrides unless explicitly designed to.
- Production and staging inject real environment values.
- Libraries do not load environment files implicitly; app/CLI/test boundaries own loading.

Adapt this policy to the actual runtime and keep `.gitignore`, tests, containers, and deployment docs aligned.

## Database, schema, or generated contracts

1. Edit __SOURCE_OF_TRUTH_PATH__.
2. Run `__GENERATION_COMMAND__`.
3. Review generated output or migrations in __GENERATED_PATH__.
4. Apply locally with `__MIGRATION_OR_APPLY_COMMAND__`.
5. Run `__VALIDATION_COMMAND__` and confirm no unexplained drift.

Remove this section when the repository has no generated/schema workflow.

## Conventions

- __LANGUAGE_MODULE_AND_STRICTNESS_POLICY__
- __FILENAME_AND_IMPORT_POLICY__
- __GENERATED_FILE_POLICY__
- __BOUNDARY_VALIDATION_POLICY__
- __TEST_PLACEMENT_AND_BEHAVIOR_POLICY__

Keep this list repository-specific. Tool-owned formatting rules do not need prose duplication.

## Release and deployment

__EXPLAIN_TRIGGER_ARTIFACT_ENVIRONMENT_MIGRATION_ORDER_AND_ROLLBACK__

Remove this section until the release/deploy contract is real and verified.

## More context

<!-- TODO(git-setup-repo): keep only links that exist in this repository. -->
- [`AGENTS.md`](AGENTS.md) — project-specific coding-agent rules.
- [`docs/README.md`](docs/README.md) — durable context and reading order.
- [`__SUBSYSTEM_README__`](__SUBSYSTEM_README__) — __SUBSYSTEM_SCOPE__.
- __TRACKER_OR_ROADMAP_LINK__
