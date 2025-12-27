<script lang="ts">
  import { siteConfig } from '$lib/siteConfig';
</script>

<svelte:head>
  <title>Search • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Search</h1>
  </header>

<p>Search UI scaffold. Separate EN/ES indexes will be generated later.</p>
<p><code>/static/search-en.json</code> and <code>/static/search-es.json</code> (planned)</p>

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
