"""Serving the built single-page app.

Client-side routes such as `/shopping-list` have no file on disk, so anything
that is not a real file falls back to `index.html` for the SPA to route --
otherwise a refresh or a shared link 404s. The fallback must not swallow the
API: an unmatched `/api/...` path is a genuine 404, or a typo'd fetch receives
HTML with a 200 and fails later on `response.json()`.
"""

import logging
from pathlib import Path, PurePosixPath

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

API_PREFIX = "api"


def register_spa(app: FastAPI, static_dir: Path) -> None:
    """Register the SPA catch-all; call it after every API router."""
    root = static_dir.resolve()
    index = root / "index.html"

    # A missing build is a warning, not an error: the backend has to run
    # before the frontend has ever been built.
    if not index.is_file():
        logger.warning(
            "No SPA build found at %s - serving the API only. "
            "Run `just frontend build` to create one.",
            root,
        )

    # A FastAPI route takes its methods literally, so `@app.get` alone
    # answers uptime checks and link-preview crawlers with a 405.
    @app.api_route("/{spa_path:path}", methods=["GET", "HEAD"], include_in_schema=False)
    async def serve_spa(spa_path: str) -> FileResponse:
        if spa_path == API_PREFIX or spa_path.startswith(f"{API_PREFIX}/"):
            raise HTTPException(status_code=404)

        requested = (root / spa_path).resolve()
        # Encoded `..` segments escape the build directory otherwise. Browsers
        # normalise them away; a raw HTTP client does not.
        if requested.is_relative_to(root) and requested.is_file():
            return FileResponse(requested)

        # An extension asks for a file, not a client-side route: a tab
        # outliving its build wants a clean 404, not a shell that fails
        # opaquely on the module MIME type.
        if PurePosixPath(spa_path).suffix:
            raise HTTPException(status_code=404)

        # Resolved per request, not at startup: `just backend dev` watches
        # src/, so a first build would otherwise need a restart. A build
        # missing in production is a 404 too -- `FileResponse` would raise.
        if not index.is_file():
            raise HTTPException(status_code=404)

        # Heuristically cached otherwise, so a client can boot a stale shell
        # and request assets the deploy deleted. The ETag keeps the forced
        # revalidation cheap.
        return FileResponse(index, headers={"Cache-Control": "no-cache"})
