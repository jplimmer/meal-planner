# Meal Planner

A self-hosted weekly dinner planner: suggests recipes, lets you accept/reject and
swap them out, and generates a shopping list — usable from a phone, shared
between one household.

Backend: FastAPI (Python) · Frontend: Svelte/Vite SPA · Storage: SQLite ·
Hosted on a Raspberry Pi via Docker, accessed over Tailscale.

The app has no login: Tailscale is its only access control, so it must never be
reachable except through the tailnet — see
[ADR 0001](docs/adr/0001-tailscale-is-the-access-boundary.md).

## Documentation

- [CONTEXT.md](CONTEXT.md) — the domain glossary
- [docs/adr/](docs/adr/) — architectural decisions and why they were made

## Prerequisites

- [just](https://just.systems) — runs every task in this repo
- [pre-commit](https://pre-commit.com/) — runs the formatters and type checks
  on each commit
- Each package's own prerequisites — see [backend/README.md](backend/README.md)
  and [frontend/README.md](frontend/README.md)

## Development

Open `meal-planner.code-workspace` rather than the repo folder. The Biome
extension resolves its config and binary relative to the workspace folder, so
`frontend/` needs to be one — opened at the repo root it finds neither.

Set up each package as its README describes. From the repo root, `just check`
runs everything CI gates on; `just --list` shows the rest.

Install the hooks once (pre-commit itself can come from `uv`):

    uv tool install pre-commit
    pre-commit install

After that, hooks run automatically on `git commit`. To run them on demand:

    pre-commit run --all-files
