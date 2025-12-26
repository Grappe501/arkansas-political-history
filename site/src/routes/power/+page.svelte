<script lang="ts">
	import archive from '$lib/generated/archive-index.json';

	const powerItems = archive.items.filter((i) => i.section === 'frameworks');
</script>

<main class="page">
	<h1>Power in Arkansas</h1>
	<p class="lede">
		A framework for seeing the machine: rules, courts, money, narrative, gatekeepers, and enforcement.
	</p>

	<section class="panel">
		<h2>Framework entries</h2>

		{#if powerItems.length === 0}
			<p>No framework entries yet. Add files under <code>/content/frameworks</code>.</p>
		{:else}
			<ul class="list">
				{#each powerItems as item}
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
