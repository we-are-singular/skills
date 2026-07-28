# Project Documentation And Repository Metadata

Use this reference to create or improve the root README, workspace file, environment contract, PR guidance, and public repository hygiene.

## Contents

- Documentation ownership
- Root README recipe
- Workspace recipe
- Environment documentation
- Git and pull request guidance
- Public repository hygiene
- Documentation validation

## Documentation Ownership

Give each document one job:

- Root `README.md`: product/repository definition, quick start, commands, structure, operational map, and links.
- `docs/README.md`: deeper context, durable decisions, reading order, ADR/spec/plan index, and domain glossary.
- `AGENTS.md`: concise project-specific rules, boundaries, verification commands, and boot sequence for coding agents.
- App/package README: subsystem ownership, local commands, contracts, and operational caveats.
- ADRs/specs: decisions and requirements that should not be rewritten as generic onboarding prose.

Do not duplicate the same setup procedure across several files. Put the shortest working path in the root README and link to deeper troubleshooting or subsystem docs.

## Root README Recipe

Use `assets/templates/README.md` as a section menu, not a form that must retain every heading.

The template marks links to `docs/README.md`, `AGENTS.md`, and subsystem docs as conditional. Keep each only when the target exists; do not create empty documents merely to satisfy the template.

Recommended order:

1. **Name and one-paragraph definition.** State what the repository delivers, for whom, and its important constraint or boundary.
2. **Context pointer.** Link to the canonical docs index and explain what the root README owns.
3. **Project decisions.** List stable architecture/runtime choices that a contributor must understand before changing code.
4. **Prerequisites.** Runtime, package manager, Docker, and external CLIs with version sources.
5. **Quick start.** Install, provision when needed, and start development in the fewest commands.
6. **Useful local endpoints.** Only real URLs/ports, with safe local connection details when helpful.
7. **Commands.** Development, verification, coverage, build, database/schema, and workspace examples.
8. **Seed/sample data.** State whether provisioning seeds data; keep destructive or production-sensitive steps explicit.
9. **Structure.** A compact tree with ownership comments.
10. **Architecture/package boundaries.** Explain which app/package owns routes, state, schemas, persistence, providers, UI, generated contracts, shared toolchains, and singleton/peer hosts.
11. **Environment files.** Precedence, committed versus ignored files, and test isolation.
12. **Schema/generated workflow.** Source file, generation command, migration/apply command, and committed outputs.
13. **Conventions.** Only repository-specific rules not already obvious from tools.
14. **More context.** AGENTS, docs index, subsystem docs, API docs, tracker, and operations.

Lead with runnable onboarding, not badges or a dependency inventory. A tech-stack table is useful only when it helps contributors choose the right package or tool.

Never copy another product's language, architecture, people, tracker keys, domains, ports, environment values, seed data, or provider details. Replace template placeholders with facts verified in the target repository.

## Workspace Recipe

Name the file `<project-slug>.code-workspace`. The bundled `project.code-workspace` is intentionally small.

Adapt `folders` to include only real contributor entrypoints:

- root;
- each deployable app;
- shared packages;
- shared config/tooling packages;
- docs;
- ops/infrastructure;
- end-to-end tests when they are independently runnable.

Use display names that make ownership obvious. If commitlint derives scopes from these names, they are behavioral configuration: include every allowed scope, keep the final normalized token stable, and update commit examples when names change.

Keep settings relevant and repository-owned:

- Oxc lint/format enablement and format-on-save;
- framework-specific formatter overrides only for installed frameworks;
- Vitest explorer settings only when Vitest exists;
- Tailwind class functions/attributes only when the repository uses them;
- build, cache, vendor, and generated directory exclusions;
- import preferences that match tsconfig/package boundaries;
- recommended extensions needed to work on the repository.

The workspace template's `__GIT_INSTRUCTIONS_PATH__` is also conditional. Replace it with the copied instructions path only when that file exists; otherwise remove the whole commit-message-instructions setting.

Avoid personal colors, unrelated extensions, hardcoded local SDK paths, auto-approved terminal commands, launch configs that were not tested, or a copied Tailwind config path.

For a single-package repository, one root folder plus useful settings is enough. Do not invent a multi-root layout.

## Environment Documentation

Choose and document one policy. A useful application default is:

| File | Commit? | Purpose |
| --- | --- | --- |
| `.env` | only safe local defaults | shared development defaults |
| `.env.test` | safe deterministic values | tests, isolated from machine overrides |
| `.env.local` | no | developer-machine overrides and local secrets |
| `.env.example` | yes | required keys when safe defaults cannot be committed |

Rules:

- real process environment wins;
- production/staging inject values rather than reading committed development secrets;
- tests do not load `.env.local` unless the repository explicitly tests local overrides;
- env loading happens at application/CLI/test boundaries, not hidden in arbitrary libraries;
- examples use blank or unmistakably fake values;
- `.gitignore`, README, test setup, containers, and deploy docs agree.

Do not mention a reference file in `.gitignore` or README unless that file actually exists.

## Git And Pull Request Guidance

Use the bundled Git-conventions instructions and PR template only when no stronger local versions exist.

The commit guide must mirror commitlint exactly:

- allowed types;
- required/optional scopes;
- ticket prefix grammar;
- lowercase imperative subject policy;
- valid examples;
- any release branch/tag convention that actually exists.

The PR template should ask for:

- a concise description of intent;
- grouped changes;
- reviewable verification evidence;
- screenshots, logs, examples, or recordings when useful;
- deployment/migration notes only when applicable.

Do not encourage PR bodies to repeat routine lint/test/build command noise. Record those commands in the final handoff or a concise checks section only when the repository's review policy wants them.

Workflow modules such as auto-labeling, auto-assignment, blocked-label checks, dependency updates, or automated code review are optional. Before adding one, verify its app/token, labels, reviewers/teams, permissions, paths, and host-side setup. Never copy usernames or private team names into a public template.

## Public Repository Hygiene

Audit these files and host settings; create them only when their policy is known:

- `LICENSE`: ownership and license choice must come from the user/project.
- `SECURITY.md`: supported versions and private vulnerability intake.
- `CONTRIBUTING.md`: contributor setup, issue/PR flow, DCO/CLA, and conduct links.
- `CODE_OF_CONDUCT.md`: community expectations and reporting contact.
- `CODEOWNERS`: real teams/owners that exist on the host.
- issue forms/templates: only for an actual public intake process.
- dependency automation: derive ecosystems/directories from manifests and explain ignores.
- `.gitignore`: actual frameworks, env policy, caches, reports, and generated outputs.
- `.npmrc` or manager config: repository-wide install/security policy, not personal registry credentials.
- branch protection, required checks, merge strategy, vulnerability reporting, and release permissions.

Do not infer a license, security contact, reviewer, package registry, or deployment owner. These require explicit project facts.

## Documentation Validation

Follow the README from a fresh-clone perspective:

1. Prerequisites have a version source.
2. Install command matches the lockfile.
3. Provision command starts every required local/test service and is safe to repeat.
4. Development command reaches the documented app/endpoint.
5. Verification, coverage, and build commands exist and match hooks/CI.
6. Structure entries and linked files exist.
7. Documented dependency owners and peer hosts match the workspace manifests.
8. Env names match code and examples contain no secrets.
9. Commit examples pass commitlint.
10. Workspace folder paths and extension ids are valid.
11. No placeholder, stale TODO, copied name, dead link, or nonexistent script remains.

Use `rg -n '__[A-Z0-9_]+__|TODO\(git-setup-repo\)'` across changed files before handoff.
