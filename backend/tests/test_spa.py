from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from tests.conftest import ASSET_MARKER, INDEX_MARKER


def test_root_serves_the_index(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert INDEX_MARKER in response.text


def test_the_index_must_be_revalidated(client: TestClient) -> None:
    """A stale shell outlives its build and asks for deleted assets."""
    for path in ("/", "/shopping-list"):
        assert client.get(path).headers["cache-control"] == "no-cache"


def test_client_side_route_falls_back_to_the_index(client: TestClient) -> None:
    """A deep link has no file on disk, but must still boot the SPA."""
    response = client.get("/shopping-list")

    assert response.status_code == 200
    assert INDEX_MARKER in response.text


def test_head_is_served_alongside_get(client: TestClient) -> None:
    """Uptime probes and link-preview crawlers issue HEAD, not GET."""
    for path in ("/", "/shopping-list", "/assets/index-abc123.js"):
        assert client.head(path).status_code == 200


def test_build_asset_is_served(client: TestClient) -> None:
    response = client.get("/assets/index-abc123.js")

    assert response.status_code == 200
    assert ASSET_MARKER in response.text


def test_missing_build_asset_is_a_404(client: TestClient) -> None:
    """A tab outliving its build asks for a bundle that is now gone."""
    response = client.get("/assets/index-stale.js")

    assert response.status_code == 404
    assert INDEX_MARKER not in response.text


def test_unknown_api_path_is_a_json_404(client: TestClient) -> None:
    """Without the API guard, a typo'd fetch would receive HTML with a 200."""
    response = client.get("/api/helth")

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"


def test_traversal_outside_the_build_is_refused(client: TestClient, static_dir: Path) -> None:
    """A bare `/../` is collapsed by the client, so only the encoded forms
    reach the handler. Drop the containment check and this serves the file.
    """
    (static_dir.parent / "secret.txt").write_text("do not serve me")

    for path in ("/%2e%2e/secret.txt", "/..%2fsecret.txt"):
        response = client.get(path)

        assert response.status_code == 404
        assert "do not serve me" not in response.text


def test_every_server_route_lives_under_api(client: TestClient) -> None:
    """A server route outside /api shadows the client-side route of that name."""
    paths = {
        route.path
        for route in client.app.routes  # type: ignore[union-attr]
        if isinstance(getattr(route, "path", None), str)
    }

    assert {path for path in paths if not path.startswith("/api")} == {"/{spa_path:path}"}


def test_missing_build_serves_the_api_only(tmp_path: Path) -> None:
    """The backend must run before the frontend has ever been built."""
    app = create_app(Settings(static_dir=tmp_path / "never-built"))

    with TestClient(app) as client:
        assert client.get("/api/health").status_code == 200
        assert client.get("/").status_code == 404


def test_a_first_build_needs_no_restart(tmp_path: Path) -> None:
    """`just backend dev` watches src/, so dist/ appearing must still work."""
    dist = tmp_path / "dist"
    app = create_app(Settings(static_dir=dist))

    with TestClient(app) as client:
        assert client.get("/").status_code == 404

        dist.mkdir()
        (dist / "index.html").write_text(f"<!doctype html>{INDEX_MARKER}")

        response = client.get("/")
        assert response.status_code == 200
        assert INDEX_MARKER in response.text
