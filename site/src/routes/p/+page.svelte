<script lang="ts">
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	export let data: any;

	const Component = data.component;
	const title = (data.metadata?.title as string) ?? data.slug;
	const description = (data.metadata?.description as string) ?? '';
</script>

<svelte:head>
	<title>{title} — Arkansas Political History</title>
	{#if description}
		<meta name="description" content={description} />
	{/if}
</svelte:head>

<main class="page">
	<header class="page-header">
		<h1>{title}</h1>
		{#if description}
			<p class="lede">{description}</p>
		{/if}
	</header>

	<article class="md">
		<svelte:component this={Component} />
	</article>
</main>

<style>
	.page {
		max-width: 880px;
		margin: 0 auto;
		padding: 2rem 1.25rem 4rem;
	}

	.page-header {
		margin-bottom: 2rem;
		border-bottom: 1px solid rgba(0, 0, 0, 0.1);
		padding-bottom: 1rem;
	}

	h1 {
		font-size: 2rem;
		line-height: 1.2;
		margin: 0 0 0.5rem;
	}

	.lede {
		margin: 0;
		font-size: 1.1rem;
		opacity: 0.85;
	}

	.md :global(p) {
		line-height: 1.7;
		margin: 0 0 1rem;
	}

	.md :global(h2) {
		margin-top: 2.25rem;
		margin-bottom: 0.75rem;
		font-size: 1.5rem;
	}

	.md :global(h3) {
		margin-top: 1.75rem;
		margin-bottom: 0.5rem;
		font-size: 1.25rem;
	}

	.md :global(a) {
		text-decoration: underline;
	}
</style>
