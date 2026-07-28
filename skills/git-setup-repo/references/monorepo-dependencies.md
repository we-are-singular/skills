# Monorepo Dependency Ownership

Use this reference to convert a repository into a workspace or singularify an existing monorepo by minimizing repeated dependency ownership, installed copies, version drift, and app-local `node_modules`.

## Contents

- Target properties
- Assign the lowest common owner
- Singleton and peer contracts
- Example topology
- Conversion workflow
- Validation

## Target Properties

Aim for:

- one intentional version authority for each shared toolchain or runtime family;
- one resolved physical copy where compatible ranges allow it;
- small app manifests containing internal packages and genuinely app-specific dependencies;
- shared config packages that consumers import instead of repeating toolchains;
- one authoritative workspace lockfile;
- explicit dependency/peer contracts with no phantom imports hidden by hoisting.

Do not move every shared package to the root. Hoist ownership to the lowest common internal package that all real consumers already import. The root is reserved for app-agnostic repository automation.

## Assign The Lowest Common Owner

Use this order:

| Dependency kind | Preferred owner |
| --- | --- |
| Workspace runner, formatter/linter, hooks, commitlint, cleanup, coverage merge | Private workspace root |
| TypeScript, shared `tsconfig` presets, Node/React/ReactDOM ambient types | TypeScript config package |
| Vite, Vitest, coverage provider, shared Vite plugins/runners/config factories | Vite config package |
| Shared vendor capability or runtime integration | Internal domain/facade package that exposes it |
| Singleton framework runtime | One host app/shell, with reusable packages declaring compatible peers |
| Dependency or plugin used by only one deployable | That app/package |
| Published package runtime import | That package's dependency or peer contract |

The common-owner package should export a useful config or runtime facade. Do not create a dependency bucket that consumers import only to manipulate installation layout.

Root `devDependencies` should remain app-agnostic. Framework runtimes, provider SDKs, application adapters, and one-app plugins do not belong at root merely because the package manager can hoist them physically.

## Singleton And Peer Contracts

Use peer dependencies for host tools and singleton runtimes that consumers must share, such as a Vite plugin expecting Vite or a reusable UI package expecting React. Keep peer ranges compatible and broad enough to avoid unnecessary duplicate trees. A peer declares compatibility; it does not by itself identify the intended concrete provider.

Peer declarations are compatibility contracts, not extra installed copies. If the package manager supports catalogs, constraints, or root convergence controls, use them as the single version-policy source rather than repeating exact ranges throughout manifests.

Choose one explicit provider pattern:

| Pattern | Contract | Use when |
| --- | --- | --- |
| Owner plus wrapper | Config package owns tools as real dependencies and exports config plus CLI/script wrappers; consumers invoke the wrapper | Most portable way to avoid repeated tool declarations |
| Peer plus named host | Config/plugin package declares peers; one root tool host or deployable app explicitly provides concrete versions | Consumer must control a singleton/host tool |
| Private auto-installed peer hub | One private config workspace declares peers and the pinned manager installs/exposes them for all root-installed consumers | Only for a deliberate manager-specific private workspace policy |

A config package's `devDependencies` support its own development; they are not transitive providers for consumers. Likewise, an executable available only because it was hoisted to the root is not an adequate contract. If consumers run bare `vite`, `vitest`, or `tsc`, name the package that provides those binaries. To eliminate repeated declarations completely, expose an owner-package wrapper and make consumers call it.

Do not confuse deduplication with undeclared transitive imports:

- when an app imports only an internal facade, the facade owns the vendor dependency;
- when a package directly imports a runtime dependency, it declares that dependency or peer;
- when a package executes/imports a shared tool through an internal config package, use its exported wrapper or name the concrete peer provider;
- published or independently installable packages must work outside the monorepo and cannot rely on root hoisting;
- private root-installed workspaces may use a stricter centralized peer hub, but a clean isolated install must prove it.

For npm, the default hoisted layout can hide undeclared dependencies. A linked install exposes only declared dependencies and is useful for catching phantom imports before publication. Consult current package-manager documentation before choosing an install strategy.

## Example Topology

```text
root
  dev: workspace runner, Oxc, hooks, commitlint, cleanup/report merging

config/typescript
  owns: TypeScript, @types/node, @types/react, @types/react-dom
  exports: base/node/React tsconfig presets and a type-check wrapper

config/vite
  internal: config/typescript
  owns: Vite, Vitest, coverage provider, shared Vite plugins
  exports: Vite/Vitest config factories and executable wrappers

packages/ui
  internal dev: config/typescript, config/vite
  peers: React, ReactDOM
  runtime: UI-specific libraries

apps/web
  internal: packages/ui and domain packages
  runtime: host React/ReactDOM plus app-only SDKs/adapters
  dev: internal config packages plus genuinely app-only plugins
```

If four packages use React, aim for one host runtime version/copy and peer compatibility in reusable packages—not four independently installed React trees. Keep React type globals near the TypeScript config owner and shared Vite/React plugins near the Vite config owner. A plugin used by only one app stays local. If choosing the private peer-hub variant instead of wrappers, record the package-manager behavior as repository policy and prove every executable/import under its strict clean-install layout.

## Conversion Workflow

Treat monorepo conversion, package moves, dependency relocation, and new peer contracts as material decisions. Build the map and get approval before editing.

1. Inventory every workspace, direct external import, executable used by scripts/config, internal edge, and manifest dependency section.
2. Inspect the lock/resolved tree to distinguish repeated declarations from actual duplicate versions/copies.
3. Group shared families: TypeScript/types, Vite/Vitest/plugins, React runtime, testing libraries, provider SDKs, database tooling, and repo automation.
4. Assign the lowest common owner and mark each current declaration `keep`, `move`, `peer`, or `remove`.
5. Identify public/independently installable packages; preserve their complete runtime and peer contracts.
6. Choose the concrete provider/wrapper pattern for every shared executable or singleton.
7. Present the proposed package graph, moves, peer/provider changes, and any version conflicts to the user. Do not combine relocation with an unrequested upgrade-to-latest.
8. Create or adapt config/facade packages, then move dependency ownership without changing versions where possible.
9. Make consumers depend on the internal owner and import its exported config/facade/wrapper; remove redundant direct declarations only after no direct import/script still needs them.
10. Refresh the single lockfile with the pinned manager and inspect unexpected upgrades or duplicate subtrees.
11. Validate from a clean install, then run every affected workspace's lint, test, coverage, build, and runtime smoke checks.

## Validation

Start with a manifest and import audit:

```bash
rg -n '"(dependencies|devDependencies|peerDependencies|optionalDependencies)"' --glob 'package.json'
rg -n '"(react|react-dom|vite|vitest|typescript|@types/react|@types/react-dom)"' --glob 'package.json'
```

Use the package manager's current tree/explain commands to answer:

- How many versions and physical copies resolve for each shared family?
- Which workspace owns the selected version?
- Is every duplicate required by an incompatible peer/range?
- Can each package resolve every direct import under an isolated/strict layout?
- Do consumers use the internal config/facade instead of reaching through it to vendor internals?

For npm workspaces, useful current checks include:

```bash
npm ls react react-dom vite vitest typescript --all
npm explain <package>
npm find-dupes
npm install --install-strategy=linked
```

Run the linked install only in a disposable clean checkout or after the user approves lock/install-layout work. It is a phantom-dependency diagnostic, not the default repository mutation. For another package manager, use its official equivalent and strictest supported clean-install layout.

After reinstalling, run root commands and direct workspace commands. A successful root build is insufficient if task filtering or hoisting hides a broken package. Record justified duplicate versions and remaining cleanup rather than claiming perfect deduplication.

For every affected publishable package, also prove the artifact outside the workspace. With npm workspaces:

```bash
npm pack --dry-run --workspace <workspace-name>
npm pack --workspace <workspace-name> --pack-destination /tmp/package-check
```

With current pnpm, filter the package and choose an explicit output path. Use `--dry-run` only when `pnpm help pack` for the repository's pinned version lists it; older supported pnpm releases require creating the tarball and inspecting it directly.

```bash
pnpm --filter <workspace-name> --fail-if-no-match pack --dry-run
pnpm --filter <workspace-name> --fail-if-no-match pack --out '/tmp/package-check/%s-%v.tgz'
```

Use the current official equivalent for Yarn or Bun rather than translating npm flags by guesswork.

Inspect the tarball contents and packed manifest for missing build output, unwanted files, private/internal workspace protocols, and absent dependency/peer declarations. Install the tarball into a clean external temporary consumer, then import its public entrypoints and exercise one real contract. Workspace symlinks and root dev dependencies can make local tests pass while the published tarball is broken.
