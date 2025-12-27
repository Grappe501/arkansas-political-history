<a class="skip" href="#main">Skip to content</a>

<header class="top">
	<div class="wrap">
		<a class="brand" href="/" aria-label="Arkansas Political History home">
			<span class="brandTitle">Arkansas Political History</span>
			<span class="brandTag">A civic archive with moral clarity</span>
		</a>

		<nav class="nav" aria-label="Primary">
			<a href="/timeline">Timeline</a>
			<a href="/power">Power in Arkansas</a>
			<a href="/search">Search</a>
			<a href="/p/start-here">Start Here</a>
		</nav>
	</div>
</header>

<main id="main" class="main">
	<div class="content">
		<slot />
	</div>
</main>

<footer class="footer">
	<div class="wrap footerWrap">
		<p>
			Built for the people of Arkansas.
			<span class="sep">•</span>
			A
			<a class="footerLink" href="https://standuparkansas.com" target="_blank" rel="noreferrer">
				Stand Up Arkansas
			</a>
			project.
		</p>
	</div>
</footer>

<style>
	:global(html) {
		color-scheme: light;
	}

	:global(body) {
		margin: 0;
		font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial,
			"Apple Color Emoji", "Segoe UI Emoji";
		line-height: 1.55;
		color: rgba(15, 23, 42, 0.95);
		background: linear-gradient(180deg, rgba(15, 23, 42, 0.02), rgba(255, 255, 255, 1) 220px);
	}

	:global(a:focus-visible),
	:global(button:focus-visible),
	:global(input:focus-visible) {
		outline: 2px solid rgba(15, 23, 42, 0.6);
		outline-offset: 2px;
		border-radius: 0.6rem;
	}

	/* Skip link */
	.skip {
		position: absolute;
		left: -999px;
		top: 0;
		padding: 0.6rem 0.8rem;
		background: #fff;
		border: 1px solid rgba(0, 0, 0, 0.18);
		border-radius: 0.75rem;
		z-index: 9999;
	}
	.skip:focus {
		left: 0.75rem;
		top: 0.75rem;
	}

	/* Header */
	.top {
		position: sticky;
		top: 0;
		z-index: 50;
		backdrop-filter: blur(10px);
		background: rgba(255, 255, 255, 0.9);
		border-bottom: 1px solid rgba(0, 0, 0, 0.08);
	}

	.wrap {
		max-width: 1080px;
		margin: 0 auto;
		padding: 0.95rem 1.25rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 1rem;
	}

	.brand {
		display: grid;
		gap: 0.18rem;
		text-decoration: none;
		color: inherit;
	}

	.brandTitle {
		font-weight: 850;
		letter-spacing: -0.03em;
		line-height: 1.05;
	}

	.brandTag {
		font-size: 0.85rem;
		opacity: 0.7;
	}

	.nav {
		display: flex;
		gap: 0.6rem;
		flex-wrap: wrap;
		align-items: center;
	}

	.nav a {
		text-decoration: none;
		padding: 0.45rem 0.7rem;
		border-radius: 0.9rem;
		opacity: 0.92;
	}

	.nav a:hover {
		opacity: 1;
		background: rgba(15, 23, 42, 0.05);
	}

	/* Main layout */
	.main {
		padding: 1.6rem 0 2.5rem;
	}

	.content {
		max-width: 900px;
		margin: 0 auto;
		padding: 0 1.25rem;
	}

	/* --- Global “prose” styling for markdown output --- */
	.content :global(h1),
	.content :global(h2),
	.content :global(h3),
	.content :global(h4) {
		line-height: 1.15;
		letter-spacing: -0.02em;
		margin: 1.8rem 0 0.8rem;
	}

	.content :global(h1) {
		font-size: clamp(2rem, 3vw, 2.6rem);
		font-weight: 900;
		margin-top: 0;
	}

	.content :global(h2) {
		font-size: clamp(1.5rem, 2.2vw, 2rem);
		font-weight: 850;
	}

	.content :global(h3) {
		font-size: 1.25rem;
		font-weight: 800;
	}

	.content :global(p),
	.content :global(li) {
		font-size: 1.05rem;
	}

	.content :global(p) {
		margin: 0.9rem 0;
	}

	.content :global(a) {
		color: inherit;
		text-decoration-thickness: 2px;
		text-underline-offset: 3px;
	}

	.content :global(a:hover) {
		text-decoration: underline;
	}

	.content :global(ul),
	.content :global(ol) {
		margin: 0.8rem 0 1rem;
		padding-left: 1.3rem;
	}

	.content :global(li) {
		margin: 0.35rem 0;
	}

	.content :global(hr) {
		border: none;
		border-top: 1px solid rgba(0, 0, 0, 0.08);
		margin: 2rem 0;
	}

	.content :global(blockquote) {
		margin: 1.2rem 0;
		padding: 0.9rem 1rem;
		border-left: 3px solid rgba(15, 23, 42, 0.25);
		background: rgba(15, 23, 42, 0.03);
		border-radius: 0.9rem;
	}

	.content :global(code) {
		font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono",
			"Courier New", monospace;
		font-size: 0.95em;
		background: rgba(15, 23, 42, 0.05);
		border: 1px solid rgba(0, 0, 0, 0.08);
		padding: 0.12rem 0.35rem;
		border-radius: 0.5rem;
	}

	.content :global(pre) {
		overflow-x: auto;
		padding: 1rem;
		border-radius: 1rem;
		border: 1px solid rgba(0, 0, 0, 0.08);
		background: rgba(15, 23, 42, 0.04);
	}

	.content :global(pre code) {
		background: transparent;
		border: none;
		padding: 0;
		border-radius: 0;
		font-size: 0.92rem;
	}

	.content :global(table) {
		width: 100%;
		border-collapse: collapse;
		margin: 1.2rem 0;
		font-size: 0.98rem;
	}

	.content :global(th),
	.content :global(td) {
		border: 1px solid rgba(0, 0, 0, 0.08);
		padding: 0.6rem 0.7rem;
		vertical-align: top;
	}

	.content :global(th) {
		text-align: left;
		background: rgba(15, 23, 42, 0.04);
	}

	/* --- Helpers for list pages (Search/Timeline/Power) --- */
	.content :global(.panel) {
		border: 1px solid rgba(0, 0, 0, 0.08);
		border-radius: 1.25rem;
		padding: 1rem 1.1rem;
		background: rgba(255, 255, 255, 0.85);
		box-shadow: 0 1px 0 rgba(15, 23, 42, 0.04);
	}

	.content :global(.muted) {
		opacity: 0.72;
	}

	.content :global(.kicker) {
		font-size: 0.85rem;
		letter-spacing: 0.02em;
		text-transform: uppercase;
		opacity: 0.65;
		margin: 0 0 0.35rem;
	}

	/* Footer */
	.footer {
		border-top: 1px solid rgba(0, 0, 0, 0.08);
		background: rgba(255, 255, 255, 0.75);
	}

	.footerWrap {
		padding-top: 1.1rem;
		padding-bottom: 1.1rem;
	}

	.footer p {
		margin: 0;
		opacity: 0.75;
	}

	.footerLink {
		text-decoration: underline;
		text-decoration-thickness: 2px;
		text-underline-offset: 3px;
	}

	.sep {
		margin: 0 0.5rem;
		opacity: 0.5;
	}

	@media (max-width: 720px) {
		.wrap {
			align-items: flex-start;
			flex-direction: column;
		}
		.nav {
			gap: 0.35rem;
		}
	}
</style>
