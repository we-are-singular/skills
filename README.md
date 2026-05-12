# Singular Skills

A collection of Codex skills from [Singular](https://wearesingular.com).

These skills capture opinionated engineering patterns we use for TypeScript application work. They are intended to be project-agnostic: each skill starts by reading the local repository conventions, then applies the defaults encoded here when the local codebase is ambiguous or needs architectural cleanup.

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

## License

MIT. See [LICENSE](LICENSE).
