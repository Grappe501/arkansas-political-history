<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    type ArchiveItem = {
      section: string;
      slug: string;
      url: string;
      title: string;
      description: string;
      tags: string[];
      l2Topics?: string[];
      contentType?: string;
      date?: string;
      era?: string;
      place?: string;
    };
  
    export let data: {
      locale: string;
      q: string;
      l2: string;
      placeTag: string;
      section: string;
      type: string;
      placeTags: string[];
      sections: string[];
      types: string[];
      items: ArchiveItem[];
    };
  
    $: locale = data.locale ?? $page.params.locale ?? 'en';
  
    function hrefForItem(item: ArchiveItem) {
      const p = item?.url?.startsWith('/') ? item.url : `/${item?.url ?? ''}`;
      return `/${locale}${p}`;
    }
  
    function prettySection(s: string) {
      if (!s) return '';
      return s.charAt(0).toUpperCase() + s.slice(1);
    }
  
    function prettyType(t: string) {
      const key = (t ?? '').toLowerCase();
      switch (key) {
        case 'lesson':
          return 'Lesson';
        case 'explainer':
          return 'Explainer';
        case 'framework':
          return 'Framework';
        case 'case':
          return 'Case File';
        case 'timeline':
          return 'Timeline';
        case 'source':
          return 'Source';
        case 'reference':
          return 'Reference';
        case 'page':
        default:
          return 'Page';
      }
    }
  
    $: basePath = `/${locale}/lenses/geo`;
  
    function buildUrl(next: Partial<{ q: string; l2: string; place: string; section: string; type: string }>) {
      const u = new URL($page.url);
      u.pathname = basePath;
  
      const params = u.searchParams;
  
      // Keep existing values unless overwritten
      const q = next.q ?? data.q ?? '';
      const l2 = next.l2 ?? data.l2 ?? '';
      const place = next.place ?? data.placeTag ?? '';
      const section = next.section ?? data.section ?? '';
      const type = next.type ?? data.type ?? '';
  
      params.set('q', q);
      if (l2) params.set('l2', l2); else params.delete('l2');
      if (place) params.set('place', place); else params.delete('place');
      if (section) params.set('section', section); else params.delete('section');
      if (type) params.set('type', type); else params.delete('type');
  
      // Keep URL clean
      if (!q) params.delete('q');
  
      return u.pathname + (params.toString() ? `?${params.toString()}` : '');
    }
  </script>
  
  <svelte:head>
    <title>Geography Lens • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <nav class="crumbs" aria-label="Breadcrumb">
      <a class="crumb" href={`/${locale}/lenses`}>Lens Views</a>
      <span class="sep" aria-hidden="true">/</span>
      <span class="current" aria-current="page">Geography</span>
    </nav>
  
    <header class="hdr">
      <h1>Geography Lens</h1>
      <p class="sub">
        This view is powered by <code>place:</code> and <code>geo:</code> tags in <code>archive-index.json</code>.
        As we add county/city/district tags, this becomes a living political geography map of Arkansas.
      </p>
    </header>
  
    <section class="controls" aria-label="Filters">
      <div class="row">
        <label class="lab" for="q">Search</label>
        <input
          id="q"
          class="input"
          type="search"
          value={data.q ?? ''}
          placeholder="Search titles, tags, and descriptions…"
          on:change={(e) => (window.location.href = buildUrl({ q: (e.target as HTMLInputElement).value }))}
        />
      </div>
  
      <div class="grid">
        <div class="row">
          <label class="lab" for="section">Section</label>
          <select
            id="section"
            class="select"
            value={data.section ?? ''}
            on:change={(e) => (window.location.href = buildUrl({ section: (e.target as HTMLSelectElement).value }))}
          >
            <option value="">All</option>
            {#each data.sections as s (s)}
              <option value={s}>{prettySection(s)}</option>
            {/each}
          </select>
        </div>
  
        <div class="row">
          <label class="lab" for="type">Type</label>
          <select
            id="type"
            class="select"
            value={data.type ?? ''}
            on:change={(e) => (window.location.href = buildUrl({ type: (e.target as HTMLSelectElement).value }))}
          >
            <option value="">All</option>
            {#each data.types as t (t)}
              <option value={t}>{prettyType(t)}</option>
            {/each}
          </select>
        </div>
  
        <div class="row">
          <label class="lab" for="place">Place / Geo tag</label>
          <select
            id="place"
            class="select"
            value={data.placeTag ?? ''}
            on:change={(e) => (window.location.href = buildUrl({ place: (e.target as HTMLSelectElement).value }))}
          >
            <option value="">All</option>
            {#each data.placeTags as p (p)}
              <option value={p}>{p}</option>
            {/each}
          </select>
        </div>
      </div>
  
      {#if data.l2}
        <div class="scoped" role="note">
          <p>
            <strong>Scoped to throughline:</strong> <code>{data.l2}</code>
            <span class="sp">•</span>
            <a class="lnk" href={buildUrl({ l2: '' })}>clear scope</a>
          </p>
        </div>
      {/if}
    </section>
  
    {#if (data.placeTags?.length ?? 0) === 0}
      <div class="empty" role="note" aria-label="No geo tags yet">
        <p><strong>No place tags found yet.</strong> That’s expected early in the build.</p>
        <p>Start tagging content with one or more of these patterns:</p>
        <pre class="code"><code>place:county:Pulaski:051
  place:city:Jacksonville
  geo:cd:AR-02
  geo:hd:35
  geo:sd:14
  place:school_district:Jacksonville-North-Pulaski</code></pre>
        <p>
          Once any item has a <code>place:</code> or <code>geo:</code> tag, it will appear in this filter list automatically.
        </p>
      </div>
    {/if}
  
    <section class="results" aria-label="Results">
      <h2>Results</h2>
      <p class="meta">{data.items.length} item(s)</p>
  
      <ul class="list" aria-label="Content list">
        {#each data.items as item (item.url)}
          <li class="li">
            <a class="card" href={hrefForItem(item)}>
              <div class="top">
                <span class="pill">{prettyType(item.contentType ?? 'page')}</span>
                {#if item.section}
                  <span class="pill subtle">{item.section}</span>
                {/if}
              </div>
  
              <div class="title">{item.title}</div>
  
              {#if item.description}
                <div class="desc">{item.description}</div>
              {/if}
  
              {#if (item.tags ?? []).some((t) => /^place:|^geo:/i.test(t))}
                <div class="tags" aria-label="Place tags">
                  {#each (item.tags ?? []).filter((t) => /^place:|^geo:/i.test(t)).slice(0, 8) as t (t)}
                    <span class="tag">{t}</span>
                  {/each}
                </div>
              {/if}
            </a>
          </li>
        {/each}
      </ul>
    </section>
  
    <style>
      .crumbs {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.95rem;
        opacity: 0.85;
        margin: 0 0 1rem 0;
      }
  
      .crumb {
        text-decoration: none;
      }
  
      .crumb:hover {
        text-decoration: underline;
      }
  
      .sep {
        opacity: 0.6;
      }
  
      .current {
        font-weight: 700;
      }
  
      .hdr {
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.75rem;
        margin-bottom: 1rem;
      }
  
      .hdr h1 {
        margin: 0 0 0.35rem 0;
      }
  
      .sub {
        margin: 0;
        opacity: 0.85;
      }
  
      .controls {
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.02);
        margin: 1rem 0;
      }
  
      :global(:root[data-resolved-theme='dark']) .controls {
        background: rgba(255, 255, 255, 0.03);
      }
  
      .row {
        display: grid;
        gap: 0.35rem;
        margin-bottom: 0.75rem;
      }
  
      .lab {
        font-weight: 700;
        font-size: 0.9rem;
        opacity: 0.9;
      }
  
      .input,
      .select {
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.6rem 0.7rem;
        background: var(--panel);
        color: var(--text);
        font: inherit;
      }
  
      .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.75rem;
        margin-top: 0.75rem;
      }
  
      .scoped {
        margin-top: 0.5rem;
        padding-top: 0.75rem;
        border-top: 1px dashed var(--border);
        opacity: 0.95;
      }
  
      .sp {
        margin: 0 0.4rem;
        opacity: 0.6;
      }
  
      .lnk {
        text-decoration: none;
      }
  
      .lnk:hover {
        text-decoration: underline;
      }
  
      .empty {
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.02);
        margin: 1rem 0;
      }
  
      :global(:root[data-resolved-theme='dark']) .empty {
        background: rgba(255, 255, 255, 0.03);
      }
  
      .code {
        margin-top: 0.75rem;
        padding: 0.9rem 1rem;
        border-radius: 14px;
        border: 1px solid var(--border);
        overflow-x: auto;
        background: rgba(0, 0, 0, 0.03);
      }
  
      :global(:root[data-resolved-theme='dark']) .code {
        background: rgba(255, 255, 255, 0.04);
      }
  
      .results h2 {
        margin-bottom: 0.25rem;
      }
  
      .meta {
        margin: 0 0 0.75rem 0;
        opacity: 0.8;
      }
  
      .list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: grid;
        gap: 0.75rem;
      }
  
      .li {
        margin: 0;
        padding: 0;
      }
  
      .card {
        display: block;
        text-decoration: none;
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.02);
        transition: transform 120ms ease, box-shadow 120ms ease;
      }
  
      :global(:root[data-resolved-theme='dark']) .card {
        background: rgba(255, 255, 255, 0.03);
      }
  
      .card:hover {
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
  
      .top {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        align-items: center;
        margin-bottom: 0.5rem;
      }
  
      .pill {
        display: inline-flex;
        align-items: center;
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        background: rgba(0, 0, 0, 0.02);
      }
  
      :global(:root[data-resolved-theme='dark']) .pill {
        background: rgba(255, 255, 255, 0.03);
      }
  
      .pill.subtle {
        font-weight: 600;
        opacity: 0.85;
      }
  
      .title {
        font-weight: 800;
        letter-spacing: -0.01em;
        margin: 0 0 0.25rem 0;
        line-height: 1.25;
      }
  
      .desc {
        opacity: 0.88;
        margin: 0.15rem 0 0.25rem 0;
      }
  
      .tags {
        margin-top: 0.65rem;
        padding-top: 0.65rem;
        border-top: 1px dashed var(--border);
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        opacity: 0.95;
      }
  
      .tag {
        display: inline-block;
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.12rem 0.5rem;
        font-size: 0.8rem;
        opacity: 0.92;
        background: rgba(0, 0, 0, 0.02);
      }
  
      :global(:root[data-resolved-theme='dark']) .tag {
        background: rgba(255, 255, 255, 0.03);
      }
    </style>
  </section>
  