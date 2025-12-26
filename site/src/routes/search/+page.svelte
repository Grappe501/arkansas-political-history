<script lang="ts">
	import archive from '$lib/generated/archive-index.json';

	type Item = (typeof archive.items)[number];

	let q = '';
	let section = 'all';
	let tag = 'all';

	const sections = ['all', ...Array.from(new Set(archive.items.map((i: Item) => i.section)))].sort();

	const allTags = ['all', ...archive.tags.map((t: any) => t.tag)];

	$: normalizedQ = q.trim().toLowerCase();

	$: results = archive.items.filter((i: Item) => {
		const okSection = section === 'all' ? true : i.section === section;
		const okTag = tag === 'all' ? true : (i.tags ?? []).includes(tag);

		if (!normalizedQ) return okSection && okTag;

		const hay = `${i.title ?? ''}\n${i.description ?? ''}\n${(i.tags ?? []).join(' ')}\n${i.url ?? ''}`.toLowerCase();
		return okSection && okTag && hay.includes(normalizedQ);
	});

	function clearFilters() {
		q = '';
		section = 'all';
		tag = 'all';
	}
</script>

<svelte:head>
	<title>Search • Arkansas Political History</title>
</svelte:head>

<section class="hero">
	<p class="kicker">Search</p>
	<h1>Find anything in the archive</h1>
	<p class="muted">
		Search across timelines, power frameworks, constitutions, legislative process, sources, and pages.
	</p>
</section>

<section class="controls panel">
	<div class="grid">
		<label class="field">
			<span class="label">Query</span>
			<input
				class="input"
				type="search"
				placeholder="Try: ‘at-large voting’, ‘1868 constitution’, ‘Buffalo watershed’..."
				bind:value={q}
			/>
		</label>

		<label class="field">
			<span class="label">Section</span>
			<select class="select" bind:value={section}>
				{#each sections as s}
					<option value={s}>{s}</option>
				{/each}
			</select>
		</label>

		<label class="field">
			<span class="label">Tag</span>
			<select class="select" bind:value={tag}>
				{#each allTags as t}
					<option value={t}>{t}</option>
				{/each}
			</select>
		</label>

		<div class="actions">
			<button class="btn" type="button" on:click={clearFilters}>Reset</button>
			<div class="count">{results.length} results</div>
		</div>
	</div>

	{#if tag === 'all'}
		<div class="chips">
			<span class="chipLabel">Popular tags</span>
			{#each archive.tags.slice(0, 12) as t}
				<button class="chip" type="button" on:click={() => (tag = t.tag)}>
					{t.tag} <span class="chipCount">{t.count}</span>
				</button>
			{/each}
		</div>
	{/if}
</section>

<section class="results">
	{#if results.length === 0}
		<div class="panel">
			<p class="muted">No matches. Try a broader search or remove filters.</p>
		</div>
	{:else}
		<div class="stack">
			{#each results as item (item.url)}
				<article class="panel card">
					<div class="meta">
						<span class="pill">{item.section}</span>
						{#if item.date}<span class="metaText">{item.date}</span>{/if}
						{#if item.era}<span class="metaText">{item.era}</span>{/if}
						{#if item.place}<span class="metaText">{item.place}</span>{/if}
					</div>

					<h2 class="title">
						<a href={item.url}>{item.title}</a>
					</h2>

					{#if item.description}
						<p class="desc">{item.description}</p>
					{/if}

					{#if item.tags?.length}
						<div class="tagRow">
							{#each item.tags.slice(0, 8) as t}
								<button class="tag" type="button" on:click={() => (tag = t)}>{t}</button>
							{/each}
						</div>
					{/if}
				</article>
			{/each}
		</div>
	{/if}
</section>

<style>
	.hero {
		margin: 0 0 1.1rem;
	}
	.hero h1 {
		margin: 0.15rem 0 0.45rem;
	}

	.controls {
		margin: 1rem 0 1.2rem;
	}

	.grid {
		display: grid;
		gap: 0.9rem;
		grid-template-columns: 1.6fr 0.7fr 0.9fr;
		align-items: end;
	}

	.field {
		display: grid;
		gap: 0.4rem;
	}

	.label {
		font-size: 0.85rem;
		opacity: 0.75;
	}

	.input,
	.select {
		width: 100%;
		padding: 0.55rem 0.65rem;
		border-radius: 0.9rem;
		border: 1px solid rgba(0, 0, 0, 0.12);
		background: rgba(255, 255, 255, 0.95);
	}

	.actions {
		display: flex;
		gap: 0.7rem;
		align-items: center;
		justify-content: flex-end;
	}

	.btn {
		padding: 0.55rem 0.8rem;
		border-radius: 0.9rem;
		border: 1px solid rgba(0, 0, 0, 0.12);
		background: rgba(15, 23, 42, 0.04);
		cursor: pointer;
	}
	.btn:hover {
		background: rgba(15, 23, 42, 0.06);
	}

	.count {
		font-size: 0.9rem;
		opacity: 0.75;
	}

	.chips {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-top: 0.85rem;
		align-items: center;
	}
	.chipLabel {
		font-size: 0.85rem;
		opacity: 0.7;
		margin-right: 0.25rem;
	}
	.chip {
		border: 1px solid rgba(0, 0, 0, 0.12);
		background: rgba(255, 255, 255, 0.9);
		padding: 0.35rem 0.6rem;
		border-radius: 999px;
		cursor: pointer;
	}
	.chip:hover {
		background: rgba(15, 23, 42, 0.04);
	}
	.chipCount {
		opacity: 0.65;
		margin-left: 0.35rem;
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

	@media (max-width: 920px) {
		.grid {
			grid-template-columns: 1fr;
		}
		.actions {
			justify-content: space-between;
		}
	}
</style>
