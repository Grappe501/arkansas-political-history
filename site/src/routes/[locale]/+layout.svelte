<script lang="ts">
  import { page } from '$app/stores';
  import { siteConfig } from '$lib/siteConfig';
  import { getTheme, setTheme } from '$lib/theme';

  // Works across SvelteKit versions (no $app/environment import)
  const isBrowser = typeof window !== 'undefined';

  $: locale = $page.params.locale ?? 'en';
  $: otherLocale = locale === 'en' ? 'es' : 'en';
  $: pathRemainder = $page.url.pathname.replace(/^\/(en|es)/, '');
  $: switchHref = `/${otherLocale}${pathRemainder}${$page.url.search}`;

  // Use a simple string union without importing types
  let theme: 'light' | 'dark' | 'system' = 'system';

  if (isBrowser) theme = getTheme();

  function toggleTheme() {
    const next =
      theme === 'light' ? 'dark'
      : theme === 'dark' ? 'system'
      : 'light';

    theme = next;
    setTheme(next);
  }

  $: contentExplorerHref = `/__content?locale=${locale}`;
  $: lensesHref = `/${locale}/lenses`;
</script>

<div class="shell">
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="/{$page.params.locale}/l2">
        {siteConfig.siteName}
        <small>Arkansas Political History • Level 2</small>
      </a>

      <nav class="nav">
        <a href="/{$page.params.locale}/l2">Level 2</a>
        <a href="/{$page.params.locale}/ideas">Ideas</a>
        <a href="/{$page.params.locale}/search">Search</a>
        <a href={lensesHref}>Lenses</a>
        <a href={contentExplorerHref}>Content</a>
        <a href="/{$page.params.locale}/l3">Level 3</a>
      </nav>

      <div class="controls">
        <a class="pill" href={switchHref} aria-label="Switch language">
          {locale === 'en' ? 'ES' : 'EN'}
        </a>

        <button class="pill" type="button" on:click={toggleTheme} aria-label="Toggle theme">
          {theme === 'light' ? '☀️' : theme === 'dark' ? '🌙' : '🖥️'}
        </button>
      </div>
    </div>
  </header>

  <main class="main">
    <slot />
  </main>
</div>

<style>
  .nav {
    margin-left: auto;
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;
  }

  .nav a {
    text-decoration: none;
    color: var(--text);
    opacity: 0.92;
  }
  .nav a:hover {
    text-decoration: underline;
    opacity: 1;
  }

  .controls {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-left: 0.75rem;
  }

  .pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 44px;
    height: 36px;
    padding: 0 0.75rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    background: var(--panel);
    color: var(--text);
    text-decoration: none;
    cursor: pointer;
    line-height: 1;
  }
  button.pill {
    font: inherit;
  }

  @media (max-width: 760px) {
    .topbar-inner {
      align-items: flex-start;
      flex-direction: column;
      gap: 0.75rem;
    }
    .nav {
      margin-left: 0;
    }
    .controls {
      margin-left: 0;
    }
  }
</style>
