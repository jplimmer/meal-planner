# meal-planner

A self-hosted weekly dinner planner for a two-person household: suggests
recipes from scraped sources, lets the household accept/reject/swap
suggestions, and produces a shopping list. FastAPI backend, Svelte/Vite SPA
frontend, SQLite storage, self-hosted on a Raspberry Pi behind Tailscale.

## Conventions

- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/).
- PRs are squash-merged into `main`.
- Code `TODO`s must reference a GitHub issue number (e.g. `TODO(#2): ...`), not
  stand alone — keeps deferred work tracked instead of rotting in comments.
- Dependency ranges are tiered: exact for formatters and linters, as tight as
  versioning allows for type checkers, ecosystem default for everything else.
  Lockfiles are committed, so this governs updates, not reproducibility.
- Toolchain versions live in the manifests, not CI — Node and pnpm in
  `frontend/package.json`, Python in `backend/pyproject.toml`.
- Every JSON route lives under `/api`; every other path is served the SPA's
  `index.html`. API routers must be registered before the SPA catch-all, since
  routes match in registration order and the catch-all matches everything.
