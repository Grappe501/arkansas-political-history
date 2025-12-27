<script lang="ts">
  import { page } from '$app/stores';
  import { siteConfig } from '$lib/siteConfig';

  $: locale = $page.params.locale ?? 'en';
</script>

<svelte:head>
  <title>Level 2 Dashboard • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Level 2 Dashboard</h1>
  </header>

  <p><strong>Purpose:</strong> doctorate-level civic power literacy for Arkansas — practical, source-backed, community-centered.</p>

  <div class="grid">
    <a class="card" href={`/${locale}/l2/foundations`}>Foundations</a>
    <a class="card" href={`/${locale}/l2/power`}>Power Map</a>
    <a class="card" href={`/${locale}/l2/money`}>Money &amp; Influence</a>
    <a class="card" href={`/${locale}/l2/process`}>Rules &amp; Process</a>
    <a class="card" href={`/${locale}/l2/people`}>People &amp; Networks</a>
    <a class="card" href={`/${locale}/l2/cases`}>Case Files</a>
    <a class="card" href={`/${locale}/l2/toolkit`}>Civic Toolkit</a>
    <a class="card" href={`/${locale}/l2/sources`}>Sources &amp; Provenance</a>
    <a class="card" href={`/${locale}/l2/trackers`}>Trackers</a>
    <a class="card" href={`/${locale}/l2/about`}>About &amp; Governance</a>
  </div>

  <style>
    .grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.8rem; }
    .card {
      display:block; padding: 1rem; border: 1px solid var(--border);
      border-radius: 14px; text-decoration:none;
      background: rgba(0,0,0,0.02);
    }
    :global(:root[data-resolved-theme="dark"]) .card { background: rgba(255,255,255,0.03); }
    .card:hover { text-decoration: underline; }
  </style>
</section>

<style>
  .page-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.75rem;
    margin-bottom: 1rem;
  }
  .page-header h1 { margin: 0; }
</style>
