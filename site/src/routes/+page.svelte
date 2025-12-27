<script lang="ts">
	import archive from '$lib/generated/archive-index.json';

	type Item = (typeof archive.items)[number];

	const items = archive.items.filter((i: Item) => i.section === 'timelines');

	const byEra = new Map<string, Item[]>();
	for (const it of items) {
		const key = (it.era && it.era.trim()) || 'Uncategorized';
		if (!byEra.has(key)) byEra.set(key, []);
		byEra.get(key)!.push(it);
	}

	const eras = Array.from(byEra.entries())
		.map(([era, list]) => ({ era, list }))
		.sort((a, b) => a.era.localeCompare(b.era));
</script>

<svelte:head>
	<title>Timeline • Arkansas Political History</title>
</svelte:head>

<section class="hero">
	<p class="kicker">Timeline</p>
	<h1>Arkansas political history — organized by era</h1>
	<p class="muted">
		Use this as a spine. Each era contains entries you can cite, share, and cross-link to power and policy.
	</p>
</section>

{#if items.length === 0}
	<div class="panel">
		<p class="muted">No timeline entries yet. Add files under <code>/content/timelines</code>.</p>
	</div>
{:else}
	<section class="grid">
		{#each eras as block (block.era)}
			<article class="panel era">
				<h2 class="eraTitle">{block.era}</h2>
				<p class="muted eraCount">{block.list.length} entries</p>

				<div class="list">
					{#each block.list.slice(0, 8) as item (item.url)}
						<a class="row" href={item.url}>
							<span class="rowTitle">{item.title}</span>
							{#if item.date}<span class="rowMeta">{item.date}</span>{/if}
						</a>
					{/each}
				</div>

				{#if block.list.length > 8}
					<p class="muted more">More entries available in this era.</p>
				{/if}
			</article>
		{/each}
	</section>
{/if}

<style>
	.hero {
		margin: 0 0 1.1rem;
	}
	.hero h1 {
		margin: 0.15rem 0 0.45rem;
	}

	.grid {
		display: grid;
		gap: 0.9rem;
		grid-template-columns: repeat(2, minmax(0, 1fr));
	}

	.era {
		padding: 1.05rem 1.1rem;
	}

	.eraTitle {
		margin: 0.1rem 0 0.2rem;
	}

	.eraCount {
		margin: 0 0 0.7rem;
	}

	.list {
		display: grid;
		gap: 0.2rem;
	}

	.row {
		display: flex;
		justify-content: space-between;
		gap: 0.75rem;
		padding: 0.45rem 0.55rem;
		border-radius: 0.85rem;
		text-decoration: none;
		color: inherit;
	}

	.row:hover {
		background: rgba(15, 23, 42, 0.04);
	}

	.rowTitle {
		font-weight: 650;
		letter-spacing: -0.01em;
	}

	.rowMeta {
		opacity: 0.7;
		font-size: 0.9rem;
		white-space: nowrap;
	}

	.more {
		margin: 0.7rem 0 0;
	}

	@media (max-width: 920px) {
		.grid {
			grid-template-columns: 1fr;
		}
	}
</style>
