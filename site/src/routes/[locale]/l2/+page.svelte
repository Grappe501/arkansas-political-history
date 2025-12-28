<script lang="ts">
  import { page } from '$app/stores';
  import { siteConfig } from '$lib/siteConfig';
  import { L2_TOPICS, l2TopicHref } from '$lib/contracts/l2Topics';

  $: locale = $page.params.locale ?? 'en';

  // Ensure stable ordering even if upstream array order changes
  $: topics = [...L2_TOPICS].sort((a, b) => a.order - b.order);
</script>

<svelte:head>
  <title>Level 2 Dashboard • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Level 2 Dashboard</h1>
  </header>

  <p>
    <strong>Purpose:</strong> doctorate-level civic power literacy for Arkansas — practical, source-backed,
    community-centered.
  </p>

  <ul class="grid" aria-label="Level 2 topics">
    {#each topics as t (t.slug)}
      <li class="grid-item">
        <a class="card" href={l2TopicHref(locale, t.slug)} aria-label={t.title}>
          <div class="card-title">{t.title}</div>
          <div class="card-desc">{t.description}</div>
        </a>
      </li>
    {/each}
  </ul>

  <style>
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
      font-weight: 700;
      letter-spacing: -0.01em;
      margin: 0 0 0.35rem 0;
    }

    .card-desc {
      font-size: 0.95rem;
      line-height: 1.25rem;
      opacity: 0.85;
    }
  </style>
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
