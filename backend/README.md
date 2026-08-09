# meal-planner-backend

FastAPI backend for meal-planner. See the [repo root README](../README.md) for
the overall project.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages the
  Python interpreter (3.14) and dependencies, nothing else needed

## Setup

    uv sync

## Common commands

    uv run pytest              # run tests
    uv run ruff check .        # lint
    uv run ruff format .       # format
    uv run pyright             # type check
