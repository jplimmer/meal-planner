from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app

INDEX_MARKER = '<div id="app"></div>'
ASSET_MARKER = "meal planner asset"


@pytest.fixture
def static_dir(tmp_path: Path) -> Path:
    """A stand-in for `frontend/dist`.

    Backend tests never depend on `pnpm build` having run, which keeps the
    backend CI job independent of the frontend.
    """
    (tmp_path / "index.html").write_text(f"<!doctype html>{INDEX_MARKER}")
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "index-abc123.js").write_text(f"console.log('{ASSET_MARKER}');")
    return tmp_path


@pytest.fixture
def client(static_dir: Path) -> Iterator[TestClient]:
    with TestClient(create_app(Settings(static_dir=static_dir))) as test_client:
        yield test_client
