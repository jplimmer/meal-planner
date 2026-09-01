export type Health = { status: "ok" };

/**
 * The path is relative, so this works unchanged against the Vite dev server
 * (which proxies /api to FastAPI) and against FastAPI serving the built SPA.
 */
export async function fetchHealth(): Promise<Health> {
	const response = await fetch("/api/health");

	if (!response.ok) {
		throw new Error(`HTTP ${response.status}`);
	}

	return (await response.json()) as Health;
}
