<script lang="ts">
    import { page } from '$app/stores';
    import { siteConfig } from '$lib/siteConfig';
  
    type Topic = {
      slug: string;
      title: string;
      description: string;
      order: number;
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
      learning?: {
        mode?: string;
        estimatedMinutes?: number | null;
        interactives?: string[];
      };
      date?: string;
      era?: string;
      place?: string;
      sourceUrl?: string;
      citation?: string;
      sourcePath?: string;
    };
  
    export let data: {
      locale: string;
      topic: Topic;
      items: ArchiveItem[];
      countsByType: Record<string, number>;
    };
  
    $: locale = data?.locale ?? $page.params.locale ?? 'en';
    $: topic = data.topic;
  
    $: items = (data.items ?? []) as ArchiveItem[];
    $: countsByType = (data.countsByType ?? {}) as Record<string, number>;
  
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
  
    function metaLine(i: ArchiveItem) {
      const parts: string[] = [];
      if (i.date) parts.push(i.date);
      if (i.era) parts.push(i.era);
      if (i.place) parts.push(i.place);
      return parts.join(' • ');
    }
  
    function itemHref(item: ArchiveItem) {
      const p = item?.url?.startsWith('/') ? item.url : `/${item?.url ?? ''}`;
      return `/${locale}${p}`;
    }
  
    function topTags(tags: string[] | undefined) {
      const t = (tags ?? []).filter(Boolean);
  
      // Prioritize the tags that help cross-link power analysis
      const priority = t.filter((x) =>
        /^decade:|^era:|^place:|^section:|^policy:|direct-democracy|courts|legislature|county|church|reconstruction|civil-rights/i.test(
          x
        )
      );
  
      const rest = t.filter((x) => !priority.includes(x));
      const merged = [...priority, ...rest];
  
      return merged.slice(0, 6);
    }
  
    $: lensGeoHref = `/${locale}/lenses/geo?l2=${encodeURIComponent(topic.slug)}`;
    $: lensDemoHref = `/${locale}/lenses/demo?l2=${encodeURIComponent(topic.slug)}`;
    $: lensPolHref = `/${locale}/lenses/political?l2=${encodeURIComponent(topic.slug)}`;
  </script>
  
  <svelte:head>
    <title>{topic.title} • Level 2 • {siteConfig.siteName}</title>
  </svelte:head>
  
  <section class="prose">
    <nav class="crumbs" aria-label="Breadcrumb">
      <a class="crumb" href={`/${locale}/l2`}>Level 2</a>
      <span class="sep" aria-hidden="true">/</span>
      <span class="current" aria-current="page">{topic.title}</span>
    </nav>
  
    <header class="topic-header">
      <h1>{topic.title}</h1>
      <p class="topic-desc">{topic.description}</p>
    </header>
  
    <!-- Lens Views: this is where geo/demographic/political interpretation lives -->
    <section class="lens-panel" aria-label="Lens views">
      <div class="lens-top">
        <h2 class="lens-title">Lens Views</h2>
        <p class="lens-sub">
          Explore this same material through different maps of power: geography, demographics, and political structure.
        </p>
      </div>
  
      <div class="lens-grid" role="list" aria-label="Lens options">
        <a class="lens-card" role="listitem" href={lensGeoHref}>
          <div class="lens-name">Geography</div>
          <div class="lens-desc">Counties • cities • districts • institutions on the ground</div>
        </a>
  
        <a class="lens-card" role="listitem" href={lensDemoHref}>
          <div class="lens-name">Demographics</div>
          <div class="lens-desc">Population composition • change over time • who is included/excluded</div>
        </a>
  
        <a class="lens-card" role="listitem" href={lensPolHref}>
          <div class="lens-name">Political Structure</div>
          <div class="lens-desc">Legislature • judiciary • executive • local government • enforcement</div>
        </a>
      </div>
  
      <div class="lens-note" role="note">
        <p>
          <strong>Build note:</strong> these lenses run directly off <code>archive-index.json</code>.
          As we add place and demographic tags, the lens views get sharper automatically.
        </p>
      </div>
    </section>
  
    <section class="topic-body">
      <h2>In this topic</h2>
  
      {#if items.length === 0}
        <div class="empty">
          <p>
            Nothing is assigned to <strong>{topic.slug}</strong> yet.
          </p>
          <p class="hint">
            To add content to this topic, set frontmatter on any markdown file:
          </p>
          <pre class="code"><code>---
  title: "Example"
  l2Topics: ["{topic.slug}"]
  contentType: "explainer"
  ---</code></pre>
        </div>
      {:else}
        <div class="stats" aria-label="Topic summary">
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
  
        <ul class="list" aria-label="Content list">
          {#each items as item (item.url)}
            <li class="list-item">
              <a class="item" href={itemHref(item)}>
                <div class="item-top">
                  <span class="pill">{prettyType(item.contentType ?? 'page')}</span>
                  {#if item.learning?.estimatedMinutes}
                    <span class="pill subtle">{item.learning.estimatedMinutes} min</span>
                  {/if}
                  {#if (item.learning?.interactives?.length ?? 0) > 0}
                    <span class="pill subtle">{item.learning?.interactives?.length} interactive</span>
                  {/if}
                </div>
  
                <div class="item-title">{item.title}</div>
  
                {#if item.description}
                  <div class="item-desc">{item.description}</div>
                {/if}
  
                {#if metaLine(item)}
                  <div class="item-meta">{metaLine(item)}</div>
                {/if}
  
                <div class="throughlines" aria-label="Cross-links and tags">
                  {#if (item.l2Topics ?? []).length > 0}
                    <div class="throughline-row">
                      <span class="k">Throughlines:</span>
                      <span class="v mono">{(item.l2Topics ?? []).join(', ')}</span>
                    </div>
                  {/if}
  
                  {#if (item.tags ?? []).length > 0}
                    <div class="tag-row">
                      {#each topTags(item.tags) as t (t)}
                        <span class="tag">{t}</span>
                      {/each}
                    </div>
                  {/if}
                </div>
              </a>
            </li>
          {/each}
        </ul>
      {/if}
  
      <div class="callout" role="note" aria-label="Experiential learning note">
        <p>
          <strong>Design intent:</strong> this topic will evolve from a reading list into an immersive
          sequence—scrollytelling lessons, interactive timelines, and “choose-your-path” civic simulations.
          We’re building the metadata contract now so the experience can scale cleanly.
        </p>
      </div>
    </section>
  
    <div class="actions">
      <a class="button" href={`/${locale}/l2`}>Back to Level 2 Dashboard</a>
    </div>
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
      font-weight: 600;
    }
  
    .topic-header {
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.75rem;
      margin-bottom: 1rem;
    }
  
    .topic-header h1 {
      margin: 0 0 0.35rem 0;
    }
  
    .topic-desc {
      margin: 0;
      opacity: 0.85;
    }
  
    .lens-panel {
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1rem;
      margin: 1rem 0 1rem 0;
      background: rgba(0, 0, 0, 0.02);
    }
  
    :global(:root[data-resolved-theme='dark']) .lens-panel {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .lens-top {
      margin-bottom: 0.75rem;
    }
  
    .lens-title {
      margin: 0 0 0.25rem 0;
    }
  
    .lens-sub {
      margin: 0;
      opacity: 0.85;
    }
  
    .lens-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 0.75rem;
      margin-top: 0.75rem;
    }
  
    .lens-card {
      display: block;
      text-decoration: none;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 0.85rem;
      background: rgba(0, 0, 0, 0.02);
      transition: transform 120ms ease, box-shadow 120ms ease;
    }
  
    :global(:root[data-resolved-theme='dark']) .lens-card {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .lens-card:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
  
    :global(:root[data-resolved-theme='dark']) .lens-card:hover {
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
  
    .lens-card:focus-visible {
      outline: 3px solid rgba(59, 130, 246, 0.65);
      outline-offset: 3px;
    }
  
    .lens-name {
      font-weight: 800;
      letter-spacing: -0.01em;
      margin-bottom: 0.25rem;
    }
  
    .lens-desc {
      opacity: 0.85;
      font-size: 0.95rem;
      line-height: 1.25rem;
    }
  
    .lens-note {
      margin-top: 0.85rem;
      padding-top: 0.75rem;
      border-top: 1px dashed var(--border);
      opacity: 0.95;
    }
  
    .empty {
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1rem;
      background: rgba(0, 0, 0, 0.02);
    }
  
    :global(:root[data-resolved-theme='dark']) .empty {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .hint {
      margin-top: 0.6rem;
      opacity: 0.85;
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
  
    .stat-num {
      font-weight: 800;
      font-size: 1.35rem;
      letter-spacing: -0.02em;
      line-height: 1.2;
    }
  
    .stat-label {
      margin-top: 0.15rem;
      opacity: 0.8;
      font-size: 0.9rem;
    }
  
    .list {
      list-style: none;
      padding: 0;
      margin: 0.75rem 0 0 0;
      display: grid;
      gap: 0.75rem;
    }
  
    .list-item {
      margin: 0;
      padding: 0;
    }
  
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
  
    .item:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
    }
  
    :global(:root[data-resolved-theme='dark']) .item:hover {
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
  
    .item:focus-visible {
      outline: 3px solid rgba(59, 130, 246, 0.65);
      outline-offset: 3px;
    }
  
    .item-top {
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
  
    .item-title {
      font-weight: 800;
      letter-spacing: -0.01em;
      margin: 0 0 0.25rem 0;
      line-height: 1.25;
    }
  
    .item-desc {
      opacity: 0.88;
      margin: 0.15rem 0 0.25rem 0;
    }
  
    .item-meta {
      opacity: 0.75;
      font-size: 0.9rem;
      margin-top: 0.2rem;
    }
  
    .throughlines {
      margin-top: 0.6rem;
      padding-top: 0.6rem;
      border-top: 1px dashed var(--border);
      opacity: 0.95;
    }
  
    .throughline-row {
      display: flex;
      gap: 0.5rem;
      align-items: baseline;
      margin-bottom: 0.35rem;
    }
  
    .k {
      font-weight: 700;
      font-size: 0.9rem;
      opacity: 0.9;
    }
  
    .v {
      font-size: 0.9rem;
      opacity: 0.85;
    }
  
    .tag-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
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
  
    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
  
    .callout {
      margin-top: 1rem;
      padding: 0.9rem 1rem;
      border: 1px solid var(--border);
      border-radius: 14px;
      background: rgba(0, 0, 0, 0.02);
    }
  
    :global(:root[data-resolved-theme='dark']) .callout {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .actions {
      margin-top: 1.25rem;
    }
  
    .button {
      display: inline-block;
      padding: 0.65rem 0.9rem;
      border-radius: 12px;
      border: 1px solid var(--border);
      text-decoration: none;
      font-weight: 600;
      background: rgba(0, 0, 0, 0.02);
    }
  
    :global(:root[data-resolved-theme='dark']) .button {
      background: rgba(255, 255, 255, 0.03);
    }
  
    .button:hover {
      text-decoration: underline;
    }
  
    .button:focus-visible {
      outline: 3px solid rgba(59, 130, 246, 0.65);
      outline-offset: 3px;
    }
  </style>
  