# meal-planner-backend

FastAPI backend for meal-planner. Serves the JSON API and, in production, the
built frontend SPA from a single process. See the
[repo root README](../README.md) for the overall project.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages the
  Python interpreter (3.14) and dependencies, nothing else needed
- [just](https://just.systems) — runs every lint/typecheck/test recipe

## Setup

    uv sync

## Running

    just backend dev

Serves <http://127.0.0.1:8000> with autoreload. Interactive API docs are at
`/api/docs`.

For frontend work, run `just frontend dev` alongside it in a second terminal
and use the Vite dev server on <http://localhost:5173> — it proxies `/api` to
this process, so the SPA calls the same relative URLs in development as in
production.

## Common commands

Every check goes through `just`, so hooks, CI and local runs cannot drift
apart:

    just backend lint          # ruff check + format --check
    just backend fix           # ruff check --fix + format
    just backend typecheck     # pyright, whole project
    just backend test          # pytest

## Layout

    src/app/
      main.py        create_app() factory, plus the `app` uvicorn imports
      config.py      Settings, read from the environment
      spa.py         serves the built SPA, with an index.html fallback
      api/health.py  the health router

### Routing

Every JSON route lives under `/api`; every other path belongs to the SPA. That
split is what lets `spa.py` answer "API or SPA?" by string prefix rather than
by consulting the route table, and it is why API routers must be registered
before the SPA catch-all — routes match in registration order, and the
catch-all matches everything.

An unmatched `/api/...` path returns a JSON 404 rather than falling back to
`index.html`, so a typo'd fetch fails loudly instead of receiving HTML.

### Configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `MEAL_PLANNER_STATIC_DIR` | `static` | Directory holding the built SPA, relative to the working directory |

The default suits the container, which copies the build to `static/` beside the
app. `just backend dev` points it at `../frontend/dist` instead. If no build is
found the app logs a warning and serves the API only, so the backend runs
before the frontend has ever been built.
