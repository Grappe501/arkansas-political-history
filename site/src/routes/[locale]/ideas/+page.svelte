<script lang="ts">
  import { page } from '$app/stores';
  import { siteConfig } from '$lib/siteConfig';

  $: locale = $page.params.locale ?? 'en';
</script>

<svelte:head>
  <title>Public Ideas (Pending Approval) • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Public Ideas (Pending Approval)</h1>
  </header>

  <p>
    This is a public intake space. Submissions are <strong>reviewed and approved</strong> before appearing in the dashboard.
  </p>

  <p>
    <a href={`/${locale}/ideas/submit`}>Submit an idea</a>
  </p>

  <hr />

  <p><em>Approved ideas list will render here later.</em></p>
  <p>Approval workflow: see <code>/docs/IDEAS_WORKFLOW.md</code></p>
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
