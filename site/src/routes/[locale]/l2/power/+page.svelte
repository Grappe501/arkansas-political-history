<script lang="ts">
  import { siteConfig } from '$lib/siteConfig';
</script>

<svelte:head>
  <title>Level 2 • power • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Level 2 • power</h1>
  </header>

<p>This section is scaffolded. Topic pages are linked below.</p>
<ul>
  <li><a href={`/${locale}/l2/power/institutions`}>institutions</a></li>
  <li><a href={`/${locale}/l2/power/chokepoints`}>chokepoints</a></li>
</ul>

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
