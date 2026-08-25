# Meal Planner

A self-hosted weekly dinner planner: suggests recipes, lets you accept/reject and
swap them out, and generates a shopping list — usable from a phone, shared
between one household.

Backend: FastAPI (Python) · Frontend: Svelte/Vite SPA · Storage: SQLite ·
Hosted on a Raspberry Pi via Docker, accessed over Tailscale.

## Development

Open `meal-planner.code-workspace` rather than the repo folder. The Biome
extension resolves its config and binary relative to the workspace folder, so
`frontend/` needs to be one — opened at the repo root it finds neither.

Each package has its own setup — see [backend/README.md](backend/README.md)
(frontend to follow).

This repo uses [pre-commit](https://pre-commit.com/) to run lint/format/type
checks before each commit:

    uv tool install pre-commit
    pre-commit install

After that, hooks run automatically on `git commit`. To run them on demand:

    pre-commit run --all-files
