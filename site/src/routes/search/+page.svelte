<script lang="ts">
	import archive from '$lib/generated/archive-index.json';

	let q = '';
	let section = 'all';

	const sections = [
		{ key: 'all', label: 'All' },
		{ key: 'pages', label: 'Pages' },
		{ key: 'timelines', label: 'Timeline' },
		{ key: 'frameworks', label: 'Power Frameworks' },
		{ key: 'constitutions', label: 'Constitutions' },
		{ key: 'legislative', label: 'Legislative Process' },
		{ key: 'sources', label: 'Sources & Provenance' }
	];

	$: results = (() => {
		const needle = q.trim().toLowerCase();
		const pool =
			section === 'all'
				? archive.items
				: archive.items.filter((i) => i.section === section);

		if (!needle) return pool.slice(0, 50);

		return pool
			.filter((i) => {
				const hay = `${i.title} ${i.description} ${i.tags.join(' ')}`.toLowerCase();
				return hay.includes(needle);
			})
			.slice(0, 50);
	})();
</script>

<main class="page">
	<h1>Search</h1>
	<p class="lede">Find pages by title, description, or tags.</p>

	<section class="controls">
		<input
			class="input"
			placeholder="Search the archive…"
			bind:value={q}
			autocapitalize="off"
			autocomplete="off"
			spellcheck="false"
		/>

		<select class="select" bind:value={section}>
			{#each sections as s}
				<option value={s.key}>{s.label}</option>
			{/each}
		</select>
	</section>

	<section class="panel">
		<h2>Results ({results.length})</h2>

		<ul class="list">
			{#each results as item}
				<li class="result">
					<div class="topline">
						<a href={item.url}>{item.title}</a>
						<span class="badge">{item.section}</span>
					</div>
					{#if item.description}
						<div class="desc">{item.description}</div>
					{/if}
					{#if item.tags?.length}
						<div class="tags">{item.tags.join(' • ')}</div>
					{/if}
				</li>
			{/each}
		</ul>
	</section>
</main>

<style>
	.page {
		max-width: 980px;
		margin: 0 auto;
		padding: 2rem 1.25rem 4rem;
	}

	.lede {
		margin: 0 0 1.25rem;
		opacity: 0.85;
	}

	.controls {
		display: flex;
		gap: 0.75rem;
		flex-wrap: wrap;
		margin-bottom: 1.25rem;
	}

	.input {
		flex: 1;
		min-width: 260px;
		padding: 0.75rem 0.85rem;
		border-radius: 10px;
		border: 1px solid rgba(0, 0, 0, 0.18);
	}

	.select {
		padding: 0.75rem 0.85rem;
		border-radius: 10px;
		border: 1px solid rgba(0, 0, 0, 0.18);
		background: white;
	}

	.panel {
		border: 1px solid rgba(0, 0, 0, 0.12);
		border-radius: 12px;
		padding: 1rem 1.25rem;
	}

	.list {
		list-style: none;
		padding: 0;
		margin: 0.75rem 0 0;
	}

	.result {
		padding: 0.85rem 0;
		border-top: 1px solid rgba(0, 0, 0, 0.08);
	}

	.result:first-child {
		border-top: none;
	}

	.topline {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 1rem;
	}

	.badge {
		font-size: 0.8rem;
		opacity: 0.7;
	}

	.desc {
		margin-top: 0.35rem;
		opacity: 0.8;
	}

	.tags {
		margin-top: 0.35rem;
		opacity: 0.65;
		font-size: 0.92rem;
	}
</style>
