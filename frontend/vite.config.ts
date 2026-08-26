import { svelte } from "@sveltejs/vite-plugin-svelte";
import { VitePWA } from "vite-plugin-pwa";
import { defineConfig } from "vitest/config";

// https://vite.dev/config/
export default defineConfig({
	plugins: [
		svelte(),
		VitePWA({
			registerType: "autoUpdate",
			workbox: {
				// Navigations are answered from the precached shell, which would
				// hide /api/docs once installed. fetch() is unaffected, so no
				// test catches this.
				navigateFallbackDenylist: [/^\/api\//],
			},
			devOptions: {
				enabled: true,
			},
			manifest: {
				name: "Meal Planner",
				short_name: "Meal Planner",
				description: "Weekly dinner planner and shopping list",
				theme_color: "#ffffff",
				background_color: "#ffffff",
				display: "standalone",
				start_url: "/",
				// TODO(#2): replace with real 192/512 PNG icons + maskable variant
				icons: [
					{
						src: "favicon.svg",
						sizes: "any",
						type: "image/svg+xml",
					},
				],
			},
		}),
	],
	server: {
		// The SPA calls relative /api paths. In production FastAPI serves both
		// the SPA and the API from one origin; this recreates that in
		// development, so no code needs an environment-dependent base URL and
		// the backend needs no CORS middleware.
		proxy: {
			"/api": "http://127.0.0.1:8000",
		},
	},
	resolve: {
		conditions: ["browser"],
	},
	test: {
		environment: "happy-dom",
		setupFiles: ["./vitest-setup.ts"],
	},
});
