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
        <p class="sub">Browse the generated archive index and click through to rendered pages.</p>
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
  
        <button class="btn" type="button" on:click={applyQuery} aria-label="Apply filter">Apply</button>
        <button class="btn subtle" type="button" on:click={clearQuery} aria-label="Clear filter">Clear</button>
      </div>
    </header>
  
    <div class="meta">
      <div><strong>Index count:</strong> {data.count}</div>
      <div><strong>Showing:</strong> {shown}</div>
      <div><strong>Generated:</strong> {data.generatedAt}</div>
      <div class="mono"><strong>Content root:</strong> {data.contentRoot}</div>
    </div>
  
    <!-- ✅ a11y fix: removed tabindex="0" from non-interactive element -->
    <div class="tableWrap" role="region" aria-label="Content list">
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
                <a class="link" href={itemHref(it.url)}>{it.title}</a>
                {#if it.description}
                  <div class="desc">{it.description}</div>
                {/if}
                <div class="tiny mono">{itemHref(it.url)}</div>
              </td>
              <td class="mono">{it.section}</td>
              <td class="mono">{it.slug}</td>
              <td class="mono">{it.contentType ?? ''}</td>
              <td class="mono">{(it.l2Topics ?? []).join(', ')}</td>
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
  
    .btn {
      height: 38px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: rgba(0, 0, 0, 0.02);
      padding: 0 0.75rem;
      cursor: pointer;
      font-weight: 600;
    }
  
    :global(:root[data-resolved-theme='dark']) .btn {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .btn.subtle {
      opacity: 0.85;
      font-weight: 600;
    }
  
    .meta {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 0.5rem;
      margin: 0 0 0.75rem 0;
      opacity: 0.9;
    }
  
    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
  
    .tableWrap {
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: auto;
    }
  
    .table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.95rem;
    }
  
    th,
    td {
      padding: 0.75rem;
      border-bottom: 1px solid var(--border);
      vertical-align: top;
    }
  
    th {
      text-align: left;
      font-size: 0.85rem;
      opacity: 0.85;
      position: sticky;
      top: 0;
      background: var(--panel);
      z-index: 1;
    }
  
    .titleCell {
      min-width: 340px;
    }
  
    .link {
      font-weight: 800;
      text-decoration: none;
    }
  
    .link:hover {
      text-decoration: underline;
    }
  
    .desc {
      margin-top: 0.25rem;
      opacity: 0.85;
    }
  
    .tiny {
      margin-top: 0.25rem;
      font-size: 0.8rem;
      opacity: 0.7;
    }
  
    .tags {
      min-width: 260px;
    }
  
    .tag {
      display: inline-block;
      margin: 0 0.3rem 0.3rem 0;
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
  
    .tag.more {
      opacity: 0.75;
    }
  
    .hint {
      margin-top: 0.85rem;
      opacity: 0.85;
    }
  </style>
  