<script lang="ts">
  import { siteConfig } from '$lib/siteConfig';
</script>

<svelte:head>
  <title>Submit an Idea • {siteConfig.siteName}</title>
</svelte:head>

<section class="prose">
  <header class="page-header">
    <h1>Submit an Idea</h1>
  </header>

<p>
  Submit an idea to improve the Arkansas Political History dashboard. We require an email to verify identity.
</p>

<form name="ideas" method="POST" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="ideas" />

  <p style="display:none;">
    <label>Don’t fill this out: <input name="bot-field" /></label>
  </p>

  <label>
    Full name<br />
    <input name="name" required />
  </label>
  <br /><br />

  <label>
    Email (required for identity verification)<br />
    <input name="email" type="email" required />
  </label>
  <br /><br />

  <label>
    County / City<br />
    <input name="location" />
  </label>
  <br /><br />

  <label>
    Idea title<br />
    <input name="title" required />
  </label>
  <br /><br />

  <label>
    Your idea (details)<br />
    <textarea name="details" rows="8" required></textarea>
  </label>
  <br /><br />

  <label>
    Links / sources (optional)<br />
    <textarea name="sources" rows="4"></textarea>
  </label>
  <br /><br />

  <button type="submit">Submit idea</button>
</form>

<p style="margin-top:1rem;">
  <strong>Note:</strong> Before Level 3 access, request a password by emailing
  <a href="mailto:standuparkansas@gmail.com">standuparkansas@gmail.com</a>.
</p>

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
