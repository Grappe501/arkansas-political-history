<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    $: locale = $page.params.locale ?? 'en';
  
    const lenses = [
      {
        slug: 'geo',
        title: 'Geography Lens',
        description: 'Counties • cities • districts • institutions on the ground.'
      },
      {
        slug: 'demo',
        title: 'Demographic Lens',
        description: 'Population composition • change over time • who is included/excluded.'
      },
      {
        slug: 'political',
        title: 'Political Structure Lens',
        description: 'Legislature • judiciary • executive • local government • enforcement.'
      }
    ];
  </script>
  
  <svelte:head>
    <title>Lens Views • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <header class="page-header">
      <h1>Lens Views</h1>
      <p class="sub">
        Same archive. Different maps. These lenses surface how power changes depending on place, population, and
        institutional structure.
      </p>
    </header>
  
    <ul class="grid" aria-label="Available lenses">
      {#each lenses as l (l.slug)}
        <li class="grid-item">
          <a class="card" href={`/${locale}/lenses/${l.slug}`}>
            <div class="card-title">{l.title}</div>
            <div class="card-desc">{l.description}</div>
          </a>
        </li>
      {/each}
    </ul>
  
    <div class="note" role="note" aria-label="Build note">
      <p>
        <strong>Build note:</strong> lenses read directly from <code>archive-index.json</code>. As we tag content with
        <code>place:</code>, <code>geo:</code>, and <code>demo:</code> tags, these pages automatically get smarter.
      </p>
    </div>
  
    <style>
      .page-header {
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
      }
  
      .page-header h1 {
        margin: 0 0 0.35rem 0;
      }
  
      .sub {
        margin: 0;
        opacity: 0.85;
      }
  
      .grid {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 0.9rem;
      }
  
      .grid-item {
        margin: 0;
        padding: 0;
      }
  
      .card {
        display: block;
        padding: 1rem;
        border: 1px solid var(--border);
        border-radius: 14px;
        text-decoration: none;
        background: rgba(0, 0, 0, 0.02);
        transition: transform 120ms ease, box-shadow 120ms ease;
      }
  
      :global(:root[data-resolved-theme='dark']) .card {
        background: rgba(255, 255, 255, 0.03);
      }
  
      .card:hover {
        text-decoration: none;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
      }
  
      :global(:root[data-resolved-theme='dark']) .card:hover {
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
      }
  
      .card:focus-visible {
        outline: 3px solid rgba(59, 130, 246, 0.65);
        outline-offset: 3px;
      }
  
      .card-title {
        font-weight: 800;
        letter-spacing: -0.01em;
        margin: 0 0 0.35rem 0;
      }
  
      .card-desc {
        font-size: 0.95rem;
        line-height: 1.25rem;
        opacity: 0.85;
      }
  
      .note {
        margin-top: 1rem;
        padding: 0.9rem 1rem;
        border: 1px solid var(--border);
        border-radius: 14px;
        background: rgba(0, 0, 0, 0.02);
      }
  
      :global(:root[data-resolved-theme='dark']) .note {
        background: rgba(255, 255, 255, 0.03);
      }
    </style>
  </section>
  