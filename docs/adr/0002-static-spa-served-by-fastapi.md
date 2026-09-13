# The frontend is a static Svelte SPA served by FastAPI

The frontend is plain Svelte, built by Vite into static files that the FastAPI
app serves alongside the JSON API. Production is a single process on the Pi with
no Node runtime; Node is needed only to build. One process keeps the SPA and API
on the same origin, with no CORS or inter-service proxy, and leaves one
container to run and restart. There is no server-side
rendering, which costs nothing for a private tool that people open on purpose
rather than find through search or link previews.

## Considered Options

- **SvelteKit**: its server features (server rendering, server-side loading,
  form actions) need a Node process alongside FastAPI. In static mode it
  produces the same output as this approach, so it stays open as a later swap
  if the app outgrows a small router.
- **FastAPI + htmx**: one language and no frontend build, but every interaction
  round-trips to the server, a poor fit for the filtering and reject/refill UI.

## Consequences

- FastAPI owns SPA routing. A catch-all falls back to `index.html` so
  client-side routes survive a refresh, which is why every JSON route lives
  under `/api` and API routers register before the catch-all.
- The Vite dev server proxies `/api` to FastAPI, so the SPA calls the same
  relative paths in development and production, and the backend needs no CORS
  middleware.
