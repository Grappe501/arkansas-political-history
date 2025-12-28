<script lang="ts">
	import { page } from '$app/stores';
	import { siteConfig } from '$lib/siteConfig';
	import { getTheme, setTheme } from '$lib/theme';

	// Locale + language switch (works across SvelteKit versions)
	const isBrowser = typeof window !== 'undefined';

	$: locale = $page.params.locale ?? 'en';
	$: otherLocale = locale === 'en' ? 'es' : 'en';
	$: pathRemainder = $page.url.pathname.replace(/^\/(en|es)(?=\/|$)/, '');
	$: switchHref = `/${otherLocale}${pathRemainder}${$page.url.search}`;

	// Theme: light/dark/system
	let theme: 'light' | 'dark' | 'system' = 'system';
	if (isBrowser) theme = getTheme();

	function toggleTheme() {
		const next = theme === 'light' ? 'dark' : theme === 'dark' ? 'system' : 'light';
		theme = next;
		setTheme(next);
	}

	// Locale-safe href helper
	function href(path: string) {
		const p = path.startsWith('/') ? path : `/${path}`;
		// special case: if caller passes "/" or "" we want "/{locale}"
		const normalized = p === '/' ? '' : p;
		return `/${locale}${normalized}`;
	}

	// Active state helper
	$: pathname = $page.url.pathname;

	function isActive(path: string) {
		const target = href(path);
		return pathname === target || pathname.startsWith(target + '/');
	}

	// Mobile menu
	let menuOpen = false;
	$: {
		// close menu on navigation
		void pathname;
		menuOpen = false;
	}

	function toggleMenu() {
		menuOpen = !menuOpen;
	}

	// Optional: dev-only content explorer link (kept, but not prominent)
	$: contentExplorerHref = `/__content?locale=${locale}`;
</script>

<a class="skip" href="#main">Skip to content</a>

<header class="top" data-menu-open={menuOpen ? 'true' : 'false'}>
	<div class="wrap">
		<a class="brand" href={href('/')} aria-label={`${siteConfig.siteName} home`}>
			<span class="brandTitle">{siteConfig.siteName}</span>
			<span class="brandTag">A civic archive with moral clarity</span>
		</a>

		<div class="right">
			<nav class="nav" aria-label="Primary">
				<a href={href('/timeline')} aria-current={isActive('/timeline') ? 'page' : undefined}
					>Timeline</a
				>
				<a href={href('/power')} aria-current={isActive('/power') ? 'page' : undefined}
					>Power in Arkansas</a
				>
				<a href={href('/lenses')} aria-current={isActive('/lenses') ? 'page' : undefined}
					>Lens Views</a
				>
				<a href={href('/l2')} aria-current={isActive('/l2') ? 'page' : undefined}>Level 2</a>
				<a href={href('/search')} aria-current={isActive('/search') ? 'page' : undefined}
					>Search</a
				>
				<a
					href={href('/p/start-here')}
					aria-current={isActive('/p/start-here') ? 'page' : undefined}
					>Start Here</a
				>

				<!-- lightweight dev link (non-disruptive) -->
				<a class="devLink" href={contentExplorerHref} title="Content Explorer">Content</a>
			</nav>

			<div class="controls" aria-label="Site controls">
				<a class="pill" href={switchHref} aria-label="Switch language">
					{locale === 'en' ? 'ES' : 'EN'}
				</a>

				<button class="pill" type="button" on:click={toggleTheme} aria-label="Toggle theme">
					{theme === 'light' ? '☀️' : theme === 'dark' ? '🌙' : '🖥️'}
				</button>

				<button
					class="pill menuBtn"
					type="button"
					on:click={toggleMenu}
					aria-label="Toggle menu"
					aria-expanded={menuOpen}
					aria-controls="mobile-menu"
				>
					<span class="menuIcon" aria-hidden="true">{menuOpen ? '✕' : '☰'}</span>
				</button>
			</div>
		</div>
	</div>

	<!-- Mobile menu -->
	<div id="mobile-menu" class="mobile" hidden={!menuOpen}>
		<div class="mobileInner">
			<a href={href('/timeline')} aria-current={isActive('/timeline') ? 'page' : undefined}
				>Timeline</a
			>
			<a href={href('/power')} aria-current={isActive('/power') ? 'page' : undefined}
				>Power in Arkansas</a
			>
			<a href={href('/lenses')} aria-current={isActive('/lenses') ? 'page' : undefined}
				>Lens Views</a
			>
			<a href={href('/l2')} aria-current={isActive('/l2') ? 'page' : undefined}>Level 2</a>
			<a href={href('/search')} aria-current={isActive('/search') ? 'page' : undefined}
				>Search</a
			>
			<a
				href={href('/p/start-here')}
				aria-current={isActive('/p/start-here') ? 'page' : undefined}
				>Start Here</a
			>
		</div>
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
		color-scheme: light dark;
	}

	:global(body) {
		margin: 0;
		font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial,
			"Apple Color Emoji", "Segoe UI Emoji";
		line-height: 1.55;
		color: var(--text, rgba(15, 23, 42, 0.95));
		background: linear-gradient(180deg, rgba(15, 23, 42, 0.02), rgba(255, 255, 255, 1) 220px);
	}

	:global(:root[data-resolved-theme='dark'] body) {
		background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(0, 0, 0, 1) 260px);
	}

	:global(a:focus-visible),
	:global(button:focus-visible),
	:global(input:focus-visible) {
		outline: 3px solid rgba(59, 130, 246, 0.65);
		outline-offset: 3px;
		border-radius: 0.75rem;
	}

	/* Skip link */
	.skip {
		position: absolute;
		left: -999px;
		top: 0;
		padding: 0.6rem 0.8rem;
		background: var(--panel, #fff);
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

	:global(:root[data-resolved-theme='dark']) .top {
		background: rgba(10, 10, 10, 0.75);
		border-bottom: 1px solid rgba(255, 255, 255, 0.12);
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

	.right {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		min-width: 0;
	}

	.brand {
		display: grid;
		gap: 0.18rem;
		text-decoration: none;
		color: inherit;
		min-width: 0;
	}

	.brandTitle {
		font-weight: 900;
		letter-spacing: -0.03em;
		line-height: 1.05;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.brandTag {
		font-size: 0.85rem;
		opacity: 0.72;
	}

	.nav {
		display: flex;
		gap: 0.35rem;
		flex-wrap: wrap;
		align-items: center;
	}

	.nav a {
		text-decoration: none;
		padding: 0.45rem 0.7rem;
		border-radius: 0.9rem;
		opacity: 0.92;
		transition: background 120ms ease, opacity 120ms ease;
	}

	.nav a:hover {
		opacity: 1;
		background: rgba(15, 23, 42, 0.06);
	}

	:global(:root[data-resolved-theme='dark']) .nav a:hover {
		background: rgba(255, 255, 255, 0.08);
	}

	.nav a[aria-current='page'] {
		opacity: 1;
		background: rgba(15, 23, 42, 0.1);
	}

	:global(:root[data-resolved-theme='dark']) .nav a[aria-current='page'] {
		background: rgba(255, 255, 255, 0.12);
	}

	.devLink {
		opacity: 0.55;
	}

	.controls {
		display: flex;
		align-items: center;
		gap: 0.45rem;
	}

	.pill {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		min-width: 44px;
		height: 36px;
		padding: 0 0.75rem;
		border-radius: 999px;
		border: 1px solid var(--border, rgba(0, 0, 0, 0.14));
		background: var(--panel, rgba(255, 255, 255, 0.75));
		color: inherit;
		text-decoration: none;
		cursor: pointer;
		line-height: 1;
	}

	:global(:root[data-resolved-theme='dark']) .pill {
		border-color: rgba(255, 255, 255, 0.16);
		background: rgba(255, 255, 255, 0.06);
	}

	button.pill {
		font: inherit;
	}

	.menuBtn {
		display: none;
		padding: 0 0.65rem;
	}

	.menuIcon {
		font-size: 1.05rem;
		line-height: 1;
	}

	/* Mobile menu panel */
	.mobile {
		border-top: 1px solid rgba(0, 0, 0, 0.08);
		background: rgba(255, 255, 255, 0.92);
		backdrop-filter: blur(10px);
	}

	:global(:root[data-resolved-theme='dark']) .mobile {
		border-top: 1px solid rgba(255, 255, 255, 0.12);
		background: rgba(10, 10, 10, 0.75);
	}

	.mobileInner {
		max-width: 1080px;
		margin: 0 auto;
		padding: 0.8rem 1.25rem 1rem;
		display: grid;
		gap: 0.35rem;
	}

	.mobileInner a {
		text-decoration: none;
		padding: 0.6rem 0.75rem;
		border-radius: 0.9rem;
		opacity: 0.95;
	}

	.mobileInner a:hover {
		background: rgba(15, 23, 42, 0.06);
	}

	:global(:root[data-resolved-theme='dark']) .mobileInner a:hover {
		background: rgba(255, 255, 255, 0.08);
	}

	.mobileInner a[aria-current='page'] {
		background: rgba(15, 23, 42, 0.1);
	}

	:global(:root[data-resolved-theme='dark']) .mobileInner a[aria-current='page'] {
		background: rgba(255, 255, 255, 0.12);
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

	:global(:root[data-resolved-theme='dark']) .footer {
		border-top: 1px solid rgba(255, 255, 255, 0.12);
		background: rgba(10, 10, 10, 0.65);
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

	@media (max-width: 900px) {
		.nav a {
			padding: 0.42rem 0.62rem;
		}
	}

	@media (max-width: 760px) {
		/* Hide desktop nav, show hamburger */
		.nav {
			display: none;
		}
		.menuBtn {
			display: inline-flex;
		}
	}

	@media (max-width: 720px) {
		.wrap {
			align-items: flex-start;
			flex-direction: column;
		}
		.right {
			width: 100%;
			justify-content: space-between;
		}
	}
</style>
