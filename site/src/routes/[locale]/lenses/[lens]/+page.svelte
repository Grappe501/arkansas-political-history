<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    type Lens = {
      slug: string;
      title: string;
      description: string;
      order: number;
      namespaces: string[];
    };
  
    type ArchiveItem = {
      section: string;
      slug: string;
      url: string;
      title: string;
      description: string;
      tags: string[];
      l2Topics?: string[];
      contentType?: string;
      learning?: { mode?: string; estimatedMinutes?: number | null; interactives?: string[] };
      date?: string;
      era?: string;
      place?: string;
    };
  
    // Make props optional to match defensive usage
    export let data: {
      locale?: string;
      lens?: Lens;
      items?: ArchiveItem[];
      countsByType?: Record<string, number>;
      facets?: { tag: string; count: number }[];
    };
  
    $: locale = data?.locale ?? $page.params.locale ?? 'en';
    $: lens = data?.lens;
    $: itemsAll = (data?.items ?? []) as ArchiveItem[];
    $: facets = (data?.facets ?? []) as { tag: string; count: number }[];
    $: countsByType = (data?.countsByType ?? {}) as Record<string, number>;
  
    let selectedFacet: string | null = null;
  
    $: items =
      selectedFacet
        ? itemsAll.filter((it) => (it.tags ?? []).includes(selectedFacet))
        : itemsAll;
  
    function prettyType(t: string) {
      const key = (t ?? '').toLowerCase();
      switch (key) {
        case 'lesson': return 'Lesson';
        case 'explainer': return 'Explainer';
        case 'framework': return 'Framework';
        case 'case': return 'Case File';
        case 'timeline': return 'Timeline';
        case 'source': return 'Source';
        case 'reference': return 'Reference';
        default: return 'Page';
      }
    }
  
    function metaLine(i: ArchiveItem) {
      const parts: string[] = [];
      if (i.date) parts.push(i.date);
      if (i.era) parts.push(i.era);
      if (i.place) parts.push(i.place);
      return parts.join(' • ');
    }
  
    function itemHref(item: ArchiveItem) {
      const raw = item?.url ?? '';
      const p = raw.startsWith('/') ? raw : `/${raw}`;
  
      // Avoid double locale prefix if url already includes it
      if (p.startsWith(`/${locale}/`)) return p;
  
      return `/${locale}${p}`;
    }
  </script>
  
  <svelte:head>
    <title>{lens?.title ?? 'Lens'} • Lens Views • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <nav class="crumbs" aria-label="Breadcrumb">
      <a class="crumb" href={`/${locale}/lenses`}>Lens Views</a>
      <span class="sep" aria-hidden="true">/</span>
      <span class="current" aria-current="page">{lens?.title ?? 'Lens'}</span>
    </nav>
  
    <header class="topic-header">
      <h1>{lens?.title ?? 'Lens'}</h1>
      <p class="topic-desc">{lens?.description ?? ''}</p>
    </header>
  
    {#if facets.length > 0}
      <div class="facet-bar" aria-label="Facet filters">
        <button
          class="chip"
          class:active={selectedFacet === null}
          type="button"
          on:click={() => (selectedFacet = null)}
        >
          All
        </button>
  
        {#each facets as f (f.tag)}
          <button
            class="chip"
            class:active={selectedFacet === f.tag}
            type="button"
            on:click={() => (selectedFacet = selectedFacet === f.tag ? null : f.tag)}
            title={`${f.tag} (${f.count})`}
          >
            {f.tag}
            <span class="n">{f.count}</span>
          </button>
        {/each}
      </div>
    {/if}
  
    <div class="stats" aria-label="Lens summary">
      <div class="stat">
        <div class="stat-num">{items.length}</div>
        <div class="stat-label">Items</div>
      </div>
  
      {#each Object.entries(countsByType).sort((a, b) => a[0].localeCompare(b[0])) as [t, n] (t)}
        <div class="stat">
          <div class="stat-num">{n}</div>
          <div class="stat-label">{prettyType(t)}</div>
        </div>
      {/each}
    </div>
  
    {#if items.length === 0}
      <div class="empty">
        <p>No results for this filter yet.</p>
      </div>
    {:else}
      <ul class="list" aria-label="Content list">
        {#each items as item (item.section + ':' + item.slug)}
          <li class="list-item">
            <a class="item" href={itemHref(item)}>
              <div class="item-top">
                <span class="pill">{prettyType(item.contentType ?? 'page')}</span>
                {#if item.learning?.estimatedMinutes}
                  <span class="pill subtle">{item.learning.estimatedMinutes} min</span>
                {/if}
              </div>
  
              <div class="item-title">{item.title}</div>
  
              {#if item.description}
                <div class="item-desc">{item.description}</div>
              {/if}
  
              {#if metaLine(item)}
                <div class="item-meta">{metaLine(item)}</div>
              {/if}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  
    <div class="actions">
      <a class="button" href={`/${locale}/lenses`}>Back to Lens Views</a>
    </div>
  
    <style>
      .crumbs {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.95rem;
        opacity: 0.85;
        margin: 0 0 1rem 0;
      }
      .crumb { text-decoration: none; }
      .crumb:hover { text-decoration: underline; }
      .sep { opacity: 0.6; }
      .current { font-weight: 600; }
  
      .topic-header {
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
        margin-bottom: 0.75rem;
      }
      .topic-header h1 { margin: 0 0 0.35rem 0; }
      .topic-desc { margin: 0; opacity: 0.88; }
  
      .facet-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin: 0.75rem 0 0.75rem 0;
      }
  
      .chip {
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.25rem 0.55rem;
        background: rgba(0,0,0,0.02);
        cursor: pointer;
        font: inherit;
        font-size: 0.85rem;
        opacity: 0.92;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
      }
      :global(:root[data-resolved-theme='dark']) .chip {
        background: rgba(255,255,255,0.03);
      }
      .chip.active {
        opacity: 1;
        font-weight: 800;
      }
      .n {
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.05rem 0.4rem;
        font-size: 0.8rem;
        opacity: 0.85;
      }
  
      .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
        gap: 0.65rem;
        margin: 0.75rem 0 1rem 0;
      }
      .stat {
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 0.75rem 0.85rem;
        background: rgba(0, 0, 0, 0.02);
      }
      :global(:root[data-resolved-theme='dark']) .stat {
        background: rgba(255, 255, 255, 0.03);
      }
      .stat-num { font-weight: 800; font-size: 1.35rem; line-height: 1.2; }
      .stat-label { margin-top: 0.15rem; opacity: 0.8; font-size: 0.9rem; }
  
      .list {
        list-style: none;
        padding: 0;
        margin: 0.75rem 0 0 0;
        display: grid;
        gap: 0.75rem;
      }
      .list-item { margin: 0; padding: 0; }
  
      .item {
        display: block;
        text-decoration: none;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.02);
        transition: transform 120ms ease, box-shadow 120ms ease;
      }
      :global(:root[data-resolved-theme='dark']) .item {
        background: rgba(255, 255, 255, 0.03);
      }
      .item:hover { transform: translateY(-1px); box-shadow: 0 6px 16px rgba(0,0,0,0.08); }
      :global(:root[data-resolved-theme='dark']) .item:hover { box-shadow: 0 6px 16px rgba(0,0,0,0.35); }
  
      .item-top { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 0.5rem; }
      .pill {
        display: inline-flex;
        align-items: center;
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
        font-size: 0.8rem;
        font-weight: 700;
        background: rgba(0, 0, 0, 0.02);
      }
      :global(:root[data-resolved-theme='dark']) .pill { background: rgba(255,255,255,0.03); }
      .pill.subtle { font-weight: 600; opacity: 0.85; }
  
      .item-title { font-weight: 800; margin: 0 0 0.25rem 0; line-height: 1.25; }
      .item-desc { opacity: 0.88; margin: 0.15rem 0 0.25rem 0; }
      .item-meta { opacity: 0.75; font-size: 0.9rem; margin-top: 0.2rem; }
  
      .actions { margin-top: 1.25rem; }
      .button {
        display: inline-block;
        padding: 0.65rem 0.9rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        text-decoration: none;
        font-weight: 600;
        background: rgba(0, 0, 0, 0.02);
      }
      :global(:root[data-resolved-theme='dark']) .button { background: rgba(255,255,255,0.03); }
    </style>
  </section>
  