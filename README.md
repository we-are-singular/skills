# Singular Skills

[![skills.sh](https://skills.sh/b/we-are-singular/skills)](https://skills.sh/we-are-singular/skills)

A collection of Agent skills from [Singular](https://wearesingular.com).

These skills capture engineering patterns we use for TypeScript application work. They are intended to be project-agnostic: each skill starts by reading the local repository conventions, then applies the defaults encoded here when the local codebase is ambiguous or needs architectural cleanup.

These skills are highly opinionated and reflect Singular's internal patterns and preferences. They are not a global best-practices guide. Anyone is welcome to use or follow them, but they intentionally encode our taste rather than universal rules.

## AGENTS

### Generic Code Agent

Install the generic `AGENTS.md` into your home agent config on Linux or macOS:

```bash
mkdir -p "$HOME/.agents" && curl -fsSL "https://raw.githubusercontent.com/we-are-singular/skills/main/AGENTS.md" -o "$HOME/.agents/AGENTS.md"
```

## Skills

### Backend Architecture

```bash
npx skills add we-are-singular/skills --skill backend-architecture
```

Use for writing, reviewing, or refactoring TypeScript/Node.js backend code. Covers APIs, middleware, services, repositories, database packages, SDKs, workers, integrations, config DSLs, tests, and backend architecture decisions.

The skill emphasizes clear backend boundaries: thin routes/controllers, composable guards, service-owned workflows, rich repositories, typed contracts, generated artifacts, app-owned adapters for external systems, and focused test coverage.

### Frontend Architecture

```bash
npx skills add we-are-singular/skills --skill frontend-architecture
```

Use for writing, reviewing, or refactoring TypeScript frontend code. Covers React components, Astro or Next.js apps, shared UI packages, client state, server-state fetching, forms, styling systems, routing, analytics, frontend tests, and frontend architecture decisions.

The skill emphasizes component ownership, shared UI primitives, controller/presentational splits, typed query and cache patterns, canonical schemas for forms, small intentional client stores, config-driven UI, accessibility, and behavior-focused tests.

### Git Commit PR

```bash
npx skills add we-are-singular/skills --skill git-commit-pr
```

Use for turning local changes into intentional commits and a draft pull request. Covers repo-specific commitlint rules, package/workspace scopes, careful staging, linear history with rebases, validation, PR templates, preview evidence, and safe push/PR creation.

The skill emphasizes per-package commits, exact-path staging, secret/artifact checks, conventional commit messages, real validation output, and an explicit confirmation step before pushing.

## License

MIT. See [LICENSE](LICENSE).
