# meal-planner-frontend

Svelte SPA for meal-planner, built by Vite into static files that the backend
serves in production. See the [repo root README](../README.md) for the overall
project, and [ADR 0002](../docs/adr/0002-static-spa-served-by-fastapi.md) for
why it is a static SPA rather than SvelteKit or a separate server.

## Prerequisites

- [pnpm](https://pnpm.io/installation) — the version is pinned by
  `packageManager` in `package.json`, and pnpm downloads the Node version set
  by `devEngines.runtime` if it isn't installed
- [just](https://just.systems) — runs every task in this project

Commands below run from `frontend/`. From the repo root, add the module name:
`just dev` becomes `just frontend dev`.

## Setup

    pnpm install

## Running

    just dev

Serves <http://localhost:5173> with hot reload. The dev server proxies `/api`
to the backend, so run `just dev` in `backend/` alongside it — the SPA calls
the same relative URLs in development as in production.

    just build

Writes the production build to `dist/`. `just dev` in `backend/` serves it on
<http://127.0.0.1:8000>, which is the closest local match to production.

## Common commands

Every task is a `just` recipe, so hooks, CI and local runs cannot drift apart.
`package.json` has no scripts:

    just check         # lint + typecheck + test, as CI runs them
    just lint          # biome check
    just fix           # biome check --write
    just typecheck     # svelte-check + tsc, whole project
    just test          # vitest, once
    just test-watch    # vitest, re-running on change

## Layout

    src/
      main.ts        mounts App into index.html
      App.svelte     the root component
      lib/api.ts     typed fetch wrappers for the backend's /api routes
    vite.config.ts   Svelte, PWA and test config, plus the /api dev proxy
    vitest-setup.ts  jest-dom matchers and per-test cleanup

### PWA

`vite-plugin-pwa` generates the manifest and service worker, and is enabled in
the dev server too. A service worker can keep serving a cached app shell after
a change, so if the page looks stale, unregister it in the browser's dev tools.

Navigations under `/api/` are excluded from the service worker's fallback to
the app shell, so `/api/docs` stays reachable once the app is installed.
