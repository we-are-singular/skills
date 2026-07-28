# JavaScript And TypeScript Quality Tooling

Use this reference to align the package manager, scripts, Oxc, Vitest, coverage, and type/framework checks.

## Contents

- Runtime and package manager
- Stable package scripts
- Oxc linting and formatting
- Vitest and coverage
- Monorepo coverage
- Migration and validation

## Runtime And Package Manager

Infer the package manager from the authoritative lockfile and `packageManager` field. Do not switch managers during repository setup unless explicitly requested.

| Manager | Frozen install | Executable invocation | Setup-node cache |
| --- | --- | --- | --- |
| npm | `npm ci --prefer-offline --include=optional` | `npm exec -- <tool>` | `cache: npm` |
| pnpm | `pnpm install --frozen-lockfile` | `pnpm exec <tool>` | `cache: pnpm` after pnpm setup |
| Yarn | `yarn install --immutable` | `yarn <tool>` | `cache: yarn` |
| Bun | `bun install --frozen-lockfile` | `bunx <tool>` | verify current official action/docs |

Declare the intended manager and version in `packageManager`; keep compatible `engines` and one runtime-version file such as `.nvmrc` or `.node-version`. CI, local docs, containers, and deploy builds must agree on the runtime and manager policy.

For an existing repository, preserve its documented runtime support unless a compatibility break is explicitly in scope. The agent's installed Node version is evidence about the agent host, not the repository baseline. For a new repository with no runtime contract, choose a currently supported LTS release that satisfies the framework and deployment target; verify the current Node release schedule rather than pinning an incidental local Current release.

Prove the resolved toolchain under that exact pin. A host-level command can pass while the lockfile contains packages whose `engines.node` reject `.nvmrc`. Use the repository's version manager or an equivalent isolated runtime to run the frozen install and checks, inspect engine warnings as contract failures, and keep `engines.node` bounded to release lines the resolved dependencies actually support.

`packageManager: "npm@<version>"` identifies the intended npm version and can enable setup-node cache detection, but `actions/setup-node` does not install that npm version. Choose one explicit npm policy:

- use the npm bundled with an exactly pinned Node release and make the declared/docs version match it; or
- install a pinned npm version before `npm ci`, then assert `npm --version` in CI.

Current npm can also enforce `devEngines.packageManager` before install, CI, and run commands. Treat that as a mismatch guard, not a bootstrap mechanism: the npm executable must already support and satisfy the policy. Check the current [npm package.json documentation](https://docs.npmjs.com/cli/configuring-npm/package-json#devengines) and [setup-node caching documentation](https://github.com/actions/setup-node#caching-global-packages-data) when adapting this.

After setup, print and compare the effective versions in the pinned environment:

```bash
node --version
<manager> --version
```

Do not broaden repository setup into unrelated framework or bundler major upgrades merely to make the newest quality tool fit. Preserve the application toolchain or present the migration as a separate compatibility decision.

Use the package manager's current official setup action. Pin actions to a current major or immutable SHA according to repository policy; do not copy a stale major from an old workflow.

## Stable Package Scripts

For a single package, add repository-local development dependencies for `typescript`, `oxlint`, `oxfmt`, `vitest`, and `@vitest/coverage-v8`, plus any framework checker and task runner the repository actually uses. Resolve compatible current versions from official docs and the target runtime; do not put `latest` in a committed manifest merely to avoid choosing versions.

For a monorepo, do not repeat that tool list in every workspace. Read `monorepo-dependencies.md` and route TypeScript/type globals through a TypeScript config owner, Vite/Vitest/coverage/shared plugins through a Vite config owner, and app-agnostic automation through the root. Consumers depend on the internal owner package instead of redeclaring the whole toolchain.

Audit dependency placement while touching manifests. Linters, formatters, test runners, coverage providers, bundlers, framework build plugins, commit tools, and local orchestration normally belong in `devDependencies`; keep a package in `dependencies` only when production execution or package consumers require it. Keep app-only dependencies local. A package that directly imports a runtime dependency must still own a valid dependency or peer contract; deduplication is not permission to rely on accidental hoisting.

For a single TypeScript package, start from this interface and adapt the build/framework commands:

```json
{
  "scripts": {
    "format": "oxfmt .",
    "format:check": "oxfmt --check .",
    "lint": "tsc --noEmit && oxlint .",
    "lint:fix": "oxlint --fix .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "build": "<existing build command>",
    "prepare": "husky"
  }
}
```

Important distinctions:

- Oxlint does not replace `tsc --noEmit`, framework checkers, schema validation, or generated-contract checks.
- `test` should be non-watch and deterministic. Keep coverage in an explicit command so normal feedback stays fast.
- `format` writes; `format:check` verifies. CI should use the check form.
- Root scripts are the public automation interface. Hooks and CI should not duplicate tool flags unless they intentionally run a narrower mode.
- A workspace task runner may replace direct commands, but every task must exist in each applicable workspace or be excluded intentionally.

For frontend frameworks, use their supported checker where it owns template/component semantics, then run Oxlint for JavaScript/TypeScript. Keep Prettier or another formatter only for file types Oxfmt does not support correctly in the installed version.

## Oxc Linting And Formatting

Use the bundled `.oxlintrc.json`, `.oxlintrc-react.json`, and `.oxfmtrc.json` as starting points. The first lint asset is TypeScript/Node-oriented; the React asset covers a mixed JavaScript/TypeScript client and Node server. Before adapting either, query current Oxc documentation for the installed `oxlint` and `oxfmt` versions.

For TypeScript React, retain the TypeScript rules in the mixed React asset and delete JavaScript-only globs only when the repository has no JavaScript source. Do not silently lose TypeScript rules merely because an existing React config began as JavaScript.

### Lint configuration

Keep the generic base focused on:

- correctness errors and suspicious/style warnings;
- unused variables, duplicate imports, debugger/alert prevention, equality, and async/promise mistakes;
- consistent type imports/exports;
- filename convention and meaningful complexity warnings;
- generated, vendored, build, cache, migration-output, and coverage exclusions;
- relaxed rules for tests where assertions, mocks, fixtures, or non-null access justify them.

Enable only plugins that correspond to real files. Put React, Astro, Svelte, Vue, test-runner, or other framework rules in targeted overrides or app-local configs. Do not declare browser globals across a server-only repository or Node globals across an edge-only runtime.

For a mixed React client and Node server:

- keep only language-version globals at the root, then enable `browser` on client globs and `node` on server, script, and config globs;
- enable the `react` plugin and at least `react/jsx-no-undef` plus `react/rules-of-hooks` for React source;
- disable `react/react-in-jsx-scope` only when the repository uses the modern automatic JSX transform;
- allow intentional side-effect style imports without permitting arbitrary unassigned imports;
- add TypeScript plugins and rules only when TypeScript files exist; remove them from a JavaScript-only repository;
- align Vitest globals with the actual import/global style instead of enabling both indiscriminately; when `globals: true` is intentional, declare only Vitest globals and disable `vitest/prefer-importing-vitest-globals` in the matching test override.

Use `oxlint --print-config <representative-file>` for one client, server, and test file. Confirm a browser file does not inherit Node globals and framework rules are active where expected.

Type-aware linting is a separate compatibility decision. Prefer it for TypeScript repositories once the current toolchain supports it, but keep the generic asset non-type-aware so it never advertises rules that silently lack semantic data. Verify the installed Oxlint package, Node runtime, TypeScript version, `oxlint-tsgolint` companion package, project references, and CLI/config contract before enabling it. Do not infer that editor type-aware support proves CI is type-aware.

Current Oxc documentation uses this shape:

```json
{
  "options": {
    "typeAware": true
  },
  "rules": {
    "typescript/no-floating-promises": "error",
    "typescript/await-thenable": "error",
    "typescript/no-misused-promises": "error"
  }
}
```

Install a compatible pinned `oxlint-tsgolint` version and prove the repository with `oxlint --type-aware` before making those rules part of `lint`. If using Oxc type diagnostics as well, evaluate `typeCheck` separately before removing `tsc --noEmit` or a framework checker.

### Formatter configuration

The baseline intentionally uses:

- 120-column print width;
- two spaces, no semicolons, double quotes, and ES5 trailing commas;
- LF line endings;
- no trailing commas in JSON;
- ignored generated/build/vendor paths.

These are defaults, not permission for a repository-wide style rewrite. Existing style wins unless formatter migration is agreed. When migrating, land the mechanical formatting separately from logic changes.

For lint-staged, use `oxfmt --no-error-on-unmatched-pattern` so unsupported or empty matches do not fail the commit. Keep JavaScript/TypeScript lint-fix and format commands sequential for the same glob to avoid concurrent writes.

## Vitest And Coverage

Start from `assets/templates/vitest.config.ts` for a single TypeScript package or as the shared base of a monorepo. Use `assets/templates/vitest.react-node.config.js` for a mixed JavaScript/TypeScript React client plus Node server; it uses Vitest projects to keep `jsdom` and `node` test environments separate while root coverage spans both. Install `jsdom` and the repository's chosen React behavior-test library when using that variant.

For a single TypeScript React app, keep the TypeScript config and change its environment and source/test globs to the real client paths. For a mixed TypeScript client/server, translate the split-project shape to TypeScript deliberately and prove both projects plus the combined coverage include; the JavaScript filename is not a reason to copy JavaScript-only globs unchanged.

Add at least one behavior test for a real exported contract when code already exists. Assert an independently stated observable value, payload, side effect, or error; do not import the expected constant from the implementation under test. Do not satisfy setup with `expect(true).toBe(true)` or a test that only restates a TypeScript type. The baseline keeps `passWithNoTests` false for a single package; monorepos may enable it only for workspaces that legitimately contain no tests while the repository-level suite still proves real behavior.

Choose deliberately:

- `environment`: `node` for backend/library code; a browser-like environment only for DOM-dependent tests;
- `include`: match actual test placement, not every file by accident;
- `setupFiles`: deterministic env/mocks that must run for each test file;
- `globalSetup`: infrastructure used once for the entire run;
- `fileParallelism`, `maxWorkers`, and isolation: serialize tests that share one real database, port, process, or mutable fixture;
- timeouts: increase only around proven cold-start or integration boundaries;
- globals: align config, types, lint globals, and test style.

Coverage should:

- use V8 unless the repository has a reason to use Istanbul;
- include source globs explicitly so untouched files appear in the report;
- exclude generated code, declarations, configs, tests, fixtures, and build output rather than hard-to-test product code;
- emit `text`, `json-summary`, and `lcov` for local diagnosis and automation;
- write to a predictable ignored directory;
- remain separate from ordinary test runs.

Inventory first-party runtime boundaries before choosing `coverage.include`: browser client, API/server, workers, libraries with executable logic, and each test-bearing workspace. For a new repository, give each boundary at least one behavior test and include its meaningful source when feasible. If a boundary is intentionally outside automated coverage, name that limitation in the setup brief and handoff, and do not label an API-only artifact as whole-repository coverage.

Do not add an arbitrary percentage during an existing-repository migration. Measure the real baseline, identify intentionally excluded surfaces, then agree on thresholds. For a new repository, choose thresholds explicitly with the user or start report-only and create a follow-up enforcement decision.

For current Vitest majors, verify migration notes before copying old coverage options. For example, removed options must not survive just because an older config accepted them.

## Monorepo Coverage

For a workspace monorepo:

1. Put common test/coverage defaults in one shared config factory.
2. Let each test-bearing workspace define `test` and `test:coverage`.
3. Have coverage runs emit blob reports to one root-owned directory.
4. Clean stale blobs before the run.
5. Force or disable task-runner caches when cached results would omit fresh coverage blobs.
6. Merge blobs with a root Vitest config whose `coverage.include` spans all intended app/package sources.
7. Produce final human and machine-readable reports in one root report directory.

Audit the task graph against package manifests. A root command can exit successfully while silently skipping a workspace whose `test:coverage` script is missing. Compare:

```bash
rg -l '"test"\s*:' --glob 'package.json'
rg -l '"test:coverage"\s*:' --glob 'package.json'
```

Document intentional exclusions. Do not claim repository coverage when only one app or language contributes.

## Migration And Validation

When replacing existing quality tools:

1. Inventory custom rules, plugins, processors, ignores, globals, resolvers, and framework integrations.
2. Run old and new lint/check commands over representative packages.
3. Classify differences as preserved rule, deliberate policy change, unsupported rule, or false positive.
4. Compare formatter output separately and keep the mechanical rewrite isolated.
5. Update editor settings, staged-file hooks, package scripts, CI, docs, and dependencies together.
6. Remove old config only after `rg` finds no caller.

Validate at minimum:

```bash
<manager> run format:check
<manager> run lint
<manager> run test
<manager> run test:coverage
<manager> run build
```

Inspect the coverage summary, not only the exit code. Confirm framework files, generated paths, and service-backed tests behave as documented.
