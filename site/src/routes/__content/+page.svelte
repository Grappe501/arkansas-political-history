<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    export let data: {
      generatedAt: string;
      contentRoot: string;
      count: number;
      locale: string;
      q: string;
      items: Array<{
        section: string;
        slug: string;
        url: string;
        title: string;
        description: string;
        tags: string[];
        l2Topics?: string[];
        contentType?: string;
        learning?: {
          mode?: string;
          estimatedMinutes?: number | null;
          interactives?: string[];
        };
        sourcePath?: string;
      }>;
    };
  
    $: locale = data.locale ?? 'en';
    $: q = data.q ?? '';
    $: items = data.items ?? [];
    $: shown = items.length;
  
    function updateParam(key: string, value: string) {
      const u = new URL($page.url);
      if (!value) u.searchParams.delete(key);
      else u.searchParams.set(key, value);
      history.replaceState({}, '', u.toString());
    }
  
    function onLocaleChange(e: Event) {
      const v = (e.currentTarget as HTMLSelectElement).value;
      updateParam('locale', v);
      location.reload();
    }
  
    function onQueryInput(e: Event) {
      const v = (e.currentTarget as HTMLInputElement).value;
      updateParam('q', v);
      // Avoid reload-on-every-keystroke; user hits Enter or clicks Apply.
    }
  
    function applyQuery() {
      location.reload();
    }
  
    function clearQuery() {
      const u = new URL($page.url);
      u.searchParams.delete('q');
      history.replaceState({}, '', u.toString());
      location.reload();
    }
  
    function itemHref(itemUrl: string) {
      const path = itemUrl?.startsWith('/') ? itemUrl : `/${itemUrl ?? ''}`;
      return `/${locale}${path}`;
    }
  </script>
  
  <svelte:head>
    <title>Content Explorer • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <header class="header">
      <div>
        <h1>Content Explorer</h1>
        <p class="sub">
          Browse the generated archive index and click through to rendered pages.
        </p>
      </div>
  
      <div class="controls" aria-label="Explorer controls">
        <label class="control">
          <span class="label">Locale</span>
          <select class="select" on:change={onLocaleChange} value={locale} aria-label="Locale">
            <option value="en">en</option>
            <option value="es">es</option>
          </select>
        </label>
  
        <label class="control grow">
          <span class="label">Filter</span>
          <input
            class="input"
            type="search"
            placeholder="Search title, description, tags, slug…"
            value={q}
            on:input={onQueryInput}
            on:keydown={(e) => e.key === 'Enter' && applyQuery()}
            aria-label="Filter content"
          />
        </label>
  
        <button class="btn" type="button" on:click={applyQuery} aria-label="Apply filter">
          Apply
        </button>
  
        <button class="btn subtle" type="button" on:click={clearQuery} aria-label="Clear filter">
          Clear
        </button>
      </div>
    </header>
  
    <div class="meta">
      <div><strong>Index count:</strong> {data.count}</div>
      <div><strong>Showing:</strong> {shown}</div>
      <div><strong>Generated:</strong> {data.generatedAt}</div>
      <div class="mono"><strong>Content root:</strong> {data.contentRoot}</div>
    </div>
  
    <div class="tableWrap" role="region" aria-label="Content list" tabindex="0">
      <table class="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Section</th>
            <th>Slug</th>
            <th>Type</th>
            <th>L2</th>
            <th>Tags</th>
          </tr>
        </thead>
        <tbody>
          {#each items as it (it.url)}
            <tr>
              <td class="titleCell">
                <a class="link" href={itemHref(it.url)}>
                  {it.title}
                </a>
                {#if it.description}
                  <div class="desc">{it.description}</div>
                {/if}
                <div class="tiny mono">{itemHref(it.url)}</div>
              </td>
              <td class="mono">{it.section}</td>
              <td class="mono">{it.slug}</td>
              <td class="mono">{it.contentType ?? ''}</td>
              <td class="mono">
                {(it.l2Topics ?? []).join(', ')}
              </td>
              <td class="tags">
                {#each (it.tags ?? []).slice(0, 8) as t (t)}
                  <span class="tag">{t}</span>
                {/each}
                {#if (it.tags ?? []).length > 8}
                  <span class="tag more">+{(it.tags ?? []).length - 8}</span>
                {/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  
    <p class="hint">
      Tip: change locale above to test `/en/*` vs `/es/*` rendering. This page is intentionally unstyled enough to be fast and honest.
    </p>
  </section>
  
  <style>
    .header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.75rem;
      margin-bottom: 1rem;
    }
  
    .sub {
      margin: 0.25rem 0 0 0;
      opacity: 0.85;
    }
  
    .controls {
      display: flex;
      gap: 0.5rem;
      align-items: flex-end;
      flex-wrap: wrap;
      justify-content: flex-end;
    }
  
    .control {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      min-width: 160px;
    }
  
    .control.grow {
      min-width: 260px;
      flex: 1 1 320px;
    }
  
    .label {
      font-size: 0.85rem;
      opacity: 0.85;
    }
  
    .input,
    .select {
      height: 38px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--text);
      padding: 0 0.75rem;
      outline: none;
    }
  
    .input:focus-visible,
    .select:focus-visible,
    .btn:focus-visible {
      outline: 3px solid rgba(59, 130, 246, 0.65);
      outline-offset: 2px;
    }
  
    .btn {
      height: 38px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: var(--panel);
      color: var(--text);
      padding: 0 0.85rem;
      cursor: pointer;
      font: inherit;
    }
  
    .btn.subtle {
      opacity: 0.9;
    }
  
    .meta {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 0.5rem 1rem;
      margin: 0 0 1rem 0;
      padding: 0.75rem;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: rgba(0, 0, 0, 0.02);
    }
  
    :global(:root[data-resolved-theme='dark']) .meta {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 0.9rem;
    }
  
    .tableWrap {
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: auto;
      background: var(--panel);
    }
  
    .table {
      width: 100%;
      border-collapse: collapse;
      min-width: 980px;
    }
  
    th, td {
      border-bottom: 1px solid var(--border);
      padding: 0.75rem;
      vertical-align: top;
      text-align: left;
    }
  
    th {
      position: sticky;
      top: 0;
      background: var(--panel);
      z-index: 1;
    }
  
    .titleCell {
      min-width: 360px;
    }
  
    .link {
      text-decoration: none;
      font-weight: 700;
      color: var(--text);
    }
  
    .link:hover {
      text-decoration: underline;
    }
  
    .desc {
      margin-top: 0.25rem;
      opacity: 0.85;
      font-size: 0.95rem;
      line-height: 1.2rem;
    }
  
    .tiny {
      margin-top: 0.35rem;
      opacity: 0.75;
      font-size: 0.8rem;
    }
  
    .tags {
      min-width: 260px;
    }
  
    .tag {
      display: inline-block;
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 0.15rem 0.5rem;
      margin: 0 0.25rem 0.25rem 0;
      font-size: 0.8rem;
      opacity: 0.95;
      background: rgba(0, 0, 0, 0.02);
    }
  
    :global(:root[data-resolved-theme='dark']) .tag {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .tag.more {
      opacity: 0.8;
    }
  
    .hint {
      margin-top: 1rem;
      opacity: 0.85;
    }
  
    @media (max-width: 760px) {
      .header {
        flex-direction: column;
        align-items: stretch;
      }
      .controls {
        justify-content: flex-start;
      }
    }
  </style>
  