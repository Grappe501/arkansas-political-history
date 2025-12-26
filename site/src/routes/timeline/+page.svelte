<script lang="ts">
	// generated at build time
	import archive from '$lib/generated/archive-index.json';

	const timelineItems = archive.items.filter((i) => i.section === 'timelines');
</script>

<main class="page">
	<h1>Timeline</h1>
	<p class="lede">
		Eras, events, and turning points — structured so people can follow how power shifts over time.
	</p>

	<section class="panel">
		<h2>Timeline entries</h2>

		{#if timelineItems.length === 0}
			<p>No timeline entries yet. Add files under <code>/content/timelines</code>.</p>
		{:else}
			<ul class="list">
				{#each timelineItems as item}
					<li>
						<a href={item.url}>{item.title}</a>
						{#if item.description}
							<div class="desc">{item.description}</div>
						{/if}
					</li>
				{/each}
			</ul>
		{/if}
	</section>
</main>

<style>
	.page {
		max-width: 980px;
		margin: 0 auto;
		padding: 2rem 1.25rem 4rem;
	}

	.lede {
		margin: 0 0 1.5rem;
		opacity: 0.85;
	}

	.panel {
		border: 1px solid rgba(0, 0, 0, 0.12);
		border-radius: 12px;
		padding: 1rem 1.25rem;
	}

	.list {
		margin: 0.75rem 0 0;
		padding-left: 1.1rem;
	}

	.desc {
		opacity: 0.75;
		margin-top: 0.25rem;
	}
</style>
