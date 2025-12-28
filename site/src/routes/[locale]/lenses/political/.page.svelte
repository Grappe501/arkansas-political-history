<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    $: locale = $page.params.locale ?? 'en';
  </script>
  
  <svelte:head>
    <title>Political Structure Lens • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <nav aria-label="Breadcrumb">
      <a href={`/${locale}/lenses`}>Lens Views</a>
      <span aria-hidden="true"> / </span>
      <span aria-current="page">Political Structure</span>
    </nav>
  
    <h1>Political Structure Lens</h1>
    <p>
      This lens is live as a route. Next step: treat institutional tags as a controlled vocabulary so we can filter by
      mechanisms of power consistently.
    </p>
  
    <pre><code>Planned tags:
  inst:legislature
  inst:judiciary
  inst:executive
  inst:local-government
  inst:boards-commissions
  inst:church-network
  mechanism:procedural-gatekeeping
  mechanism:judicial-gatekeeping
  mechanism:enforcement
  mechanism:preemption</code></pre>
  </section>
  