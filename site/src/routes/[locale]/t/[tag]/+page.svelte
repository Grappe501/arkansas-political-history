<script lang="ts">
  import { page } from '$app/stores';
  import { siteConfig } from '$lib/siteConfig';

  $: tag = $page.params.tag;
</script>

<svelte:head>
  <title>Tag: {tag} • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Tag</h1>
  </header>

  <p>Tag hub scaffold.</p>
  <p>Tag: <strong>{tag}</strong></p>
</section>

<style>
  .page-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
    margin-bottom: 1rem;
  }
  .page-header h1 {
    margin: 0;
  }
</style>
