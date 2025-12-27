<script lang="ts">
  import { siteConfig } from '$lib/siteConfig';
</script>

<svelte:head>
  <title>Level 3 • Action (Gated) • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Level 3 • Action (Gated)</h1>
  </header>

{#if siteConfig.level3Enabled}
  <p><strong>Level 3 is enabled.</strong> (Wire the action dashboard routes next.)</p>
{:else}
  <p><strong>Level 3 is gated.</strong> To request access, email <a href="mailto:standuparkansas@gmail.com">standuparkansas@gmail.com</a>.</p>
  <p>Include:</p>
  <ul>
    <li>Your full name</li>
    <li>Your phone number</li>
    <li>Your county/city</li>
    <li>How you want to help (organizing, research, outreach, etc.)</li>
  </ul>
  <p>We’ll verify identity and respond with next steps.</p>
{/if}

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
