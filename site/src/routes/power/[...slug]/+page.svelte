<script lang="ts">
	import archive from '$lib/generated/archive-index.json';

	type Item = (typeof archive.items)[number];

	let focus = 'all';

	const items = archive.items.filter((i: Item) => i.section === 'frameworks');

	const tags = Array.from(
		new Set(items.flatMap((i: Item) => i.tags ?? []).filter((t) => typeof t === 'string'))
	).sort();

	$: filtered = focus === 'all' ? items : items.filter((i: Item) => (i.tags ?? []).includes(focus));
</script>

<svelte:head>
	<title>Power in Arkansas • Arkansas Political History</title>
</svelte:head>

<section class="hero">
	<p class="kicker">Power in Arkansas</p>
	<h1>The architecture of influence</h1>
	<p class="muted">
		These frameworks explain how decisions get made: money, institutions, gatekeepers, and the rules that keep
		communities out.
	</p>
</section>

{#if items.length === 0}
	<div class="panel">
		<p class="muted">No framework entries yet. Add files under <code>/content/frameworks</code>.</p>
	</div>
{:else}
	<section class="panel controls">
		<div class="bar">
			<div class="label">Filter by tag</div>

			<div class="chips">
				<button class:active={focus === 'all'} class="chip" on:click={() => (focus = 'all')}>
					All
				</button>

				{#each tags as t}
					<button class:active={focus === t} class="chip" on:click={() => (focus = t)}>{t}</button>
				{/each}
			</div>
		</div>

		<div class="muted summary">{filtered.length} entries</div>
	</section>

	<section class="stack">
		{#each filtered as item (item.url)}
			<article class="panel card">
				<div class="meta">
					<span class="pill">framework</span>
					{#if item.place}<span class="metaText">{item.place}</span>{/if}
					{#if item.era}<span class="metaText">{item.era}</span>{/if}
				</div>

				<h2 class="title"><a href={item.url}>{item.title}</a></h2>

				{#if item.description}
					<p class="desc">{item.description}</p>
				{/if}

				{#if item.tags?.length}
					<div class="tagRow">
						{#each item.tags.slice(0, 10) as t}
							<button class="tag" type="button" on:click={() => (focus = t)}>{t}</button>
						{/each}
					</div>
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

	.controls {
		padding: 1rem 1.1rem;
		margin: 1rem 0 1.2rem;
	}

	.bar {
		display: grid;
		gap: 0.5rem;
	}

	.label {
		font-size: 0.85rem;
		opacity: 0.75;
	}

	.summary {
		margin-top: 0.8rem;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.45rem;
	}

	.chip {
		border: 1px solid rgba(0, 0, 0, 0.12);
		background: rgba(255, 255, 255, 0.9);
		padding: 0.35rem 0.65rem;
		border-radius: 999px;
		cursor: pointer;
		opacity: 0.9;
	}

	.chip:hover {
		background: rgba(15, 23, 42, 0.04);
		opacity: 1;
	}

	.chip.active {
		background: rgba(15, 23, 42, 0.07);
		border-color: rgba(15, 23, 42, 0.22);
		opacity: 1;
	}

	.stack {
		display: grid;
		gap: 0.9rem;
	}

	.card {
		padding: 1.05rem 1.1rem;
	}

	.meta {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		align-items: center;
		margin-bottom: 0.5rem;
	}

	.pill {
		font-size: 0.8rem;
		padding: 0.18rem 0.55rem;
		border-radius: 999px;
		border: 1px solid rgba(0, 0, 0, 0.12);
		background: rgba(15, 23, 42, 0.03);
	}

	.metaText {
		font-size: 0.85rem;
		opacity: 0.7;
	}

	.title {
		margin: 0.1rem 0 0.4rem;
	}

	.desc {
		margin: 0.25rem 0 0.6rem;
		opacity: 0.85;
	}

	.tagRow {
		display: flex;
		gap: 0.4rem;
		flex-wrap: wrap;
	}

	.tag {
		border: 1px solid rgba(0, 0, 0, 0.12);
		background: rgba(255, 255, 255, 0.9);
		padding: 0.25rem 0.55rem;
		border-radius: 999px;
		cursor: pointer;
		font-size: 0.9rem;
		opacity: 0.9;
	}

	.tag:hover {
		background: rgba(15, 23, 42, 0.04);
	}
</style>
