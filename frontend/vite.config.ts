import { svelte } from "@sveltejs/vite-plugin-svelte";
import { defineConfig } from "vitest/config";
import { VitePWA } from "vite-plugin-pwa";

// https://vite.dev/config/
export default defineConfig({
	plugins: [
		svelte(),
		VitePWA({
			registerType: "autoUpdate",
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
	resolve: {
		conditions: ["browser"],
	},
	test: {
		environment: "happy-dom",
		setupFiles: ["./vitest-setup.ts"],
	},
});
