"""Runtime configuration, read from the environment."""

import os
from dataclasses import dataclass
from pathlib import Path

STATIC_DIR_ENV = "MEAL_PLANNER_STATIC_DIR"

# Relative to the working directory. The image copies the built SPA to `static/`
# beside the app, so the container needs no environment variable; local runs
# point at `../frontend/dist` (see backend/justfile).
DEFAULT_STATIC_DIR = Path("static")


@dataclass(frozen=True, slots=True)
class Settings:
    """Everything that varies between environments."""

    static_dir: Path = DEFAULT_STATIC_DIR

    @classmethod
    def from_env(cls) -> Settings:
        raw = os.environ.get(STATIC_DIR_ENV)
        return cls(static_dir=Path(raw) if raw else DEFAULT_STATIC_DIR)
