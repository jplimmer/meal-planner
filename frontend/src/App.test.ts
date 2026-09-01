import { render, screen } from "@testing-library/svelte";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App.svelte";

type StubbedResponse = { ok: boolean; status: number; body?: unknown };

/** Stub `fetch`, one queued response per call. */
const respondWith = (...responses: StubbedResponse[]) => {
	const fetchMock = vi.fn();

	for (const { ok, status, body } of responses) {
		fetchMock.mockResolvedValueOnce({ ok, status, json: async () => body });
	}

	vi.stubGlobal("fetch", fetchMock);
	return fetchMock;
};

const healthy = { ok: true, status: 200, body: { status: "ok" } };
const unhealthy = { ok: false, status: 503 };

afterEach(() => {
	vi.unstubAllGlobals();
});

describe("App", () => {
	it("requests the health endpoint by relative path", async () => {
		const fetchMock = respondWith(healthy);

		render(App);
		await screen.findByText(/Connected/);

		// Relative, so dev goes through the Vite proxy and production hits
		// FastAPI directly, with no base URL anywhere in the code.
		expect(fetchMock).toHaveBeenCalledWith("/api/health");
	});

	it("reports the backend as connected when the health check succeeds", async () => {
		respondWith(healthy);

		render(App);

		expect(await screen.findByText(/Connected/)).toBeInTheDocument();
	});

	it("reports the backend as unavailable when the health check fails", async () => {
		respondWith(unhealthy);

		render(App);

		expect(await screen.findByText(/Unavailable/)).toBeInTheDocument();
		expect(await screen.findByText(/HTTP 503/)).toBeInTheDocument();
	});

	it("re-checks the backend when retried", async () => {
		const fetchMock = respondWith(unhealthy, healthy);

		render(App);
		const user = userEvent.setup();
		await user.click(await screen.findByRole("button", { name: "Retry" }));

		expect(await screen.findByText(/Connected/)).toBeInTheDocument();
		expect(fetchMock).toHaveBeenCalledTimes(2);
	});
});
