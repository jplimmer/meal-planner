# Root recipes coordinate both stacks. Each stack's own recipes live in
# backend/justfile and frontend/justfile and run from that directory —
# `just --list-submodules` shows those too.

set default-list := true

mod backend
mod frontend

# Everything CI gates on.
check: lint typecheck test

# Lint rules and formatting, both stacks.
lint:
    just backend lint
    just frontend lint

# Type check, both stacks.
typecheck:
    just backend typecheck
    just frontend typecheck

# Unit tests, both stacks.
test:
    just backend test
    just frontend test

# Apply every autofix both stacks offer. Used by the pre-commit hooks.
fix:
    just backend fix
    just frontend fix