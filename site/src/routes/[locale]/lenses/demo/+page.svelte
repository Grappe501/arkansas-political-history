<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    $: locale = $page.params.locale ?? 'en';
  </script>
  
  <svelte:head>
    <title>Demographic Lens • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <nav aria-label="Breadcrumb">
      <a href={`/${locale}/lenses`}>Lens Views</a>
      <span aria-hidden="true"> / </span>
      <span aria-current="page">Demographics</span>
    </nav>
  
    <h1>Demographic Lens</h1>
    <p>
      This lens is live as a route, but the next build step is to standardize demographic tags and connect them to
      census-based datasets (GEOID/FIPS). Once tags exist, we’ll render faceted demographic filters automatically.
    </p>
  
    <pre><code>Planned tags:
  demo:majority-black
  demo:majority-white
  demo:plurality-latino
  demo:income-quartile:1-4
  demo:urban-rural:urban|suburban|rural
  demo:population-change:decline|growth</code></pre>
  </section>
  