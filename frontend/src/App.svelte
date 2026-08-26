<script lang="ts">
import { fetchHealth } from "./lib/api";

// Kicked off at construction; reassigning re-runs the {#await} block.
let check = $state(fetchHealth());

const retry = () => {
	check = fetchHealth();
};
</script>

<main>
	<h1>Meal Planner</h1>
	<p>Weekly dinner planning for the household.</p>

	<section class="status">
		<h2>Backend</h2>
		{#await check}
			<p class="pending">Checking&hellip;</p>
		{:then health}
			<p class="ok">Connected &mdash; reported <code>{health.status}</code></p>
		{:catch error}
			<p class="failed">Unavailable &mdash; {error.message}</p>
			<button type="button" onclick={retry}>Retry</button>
		{/await}
	</section>
</main>
