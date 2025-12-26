<script lang="ts">
	export let data;
</script>

<header class="top">
	<div class="wrap">
		<a class="brand" href="/">Arkansas Political History</a>

		<nav class="nav">
			<a href="/timeline">Timeline</a>
			<a href="/power">Power in Arkansas</a>
			<a href="/search">Search</a>
			<a href="/p/start-here">Start Here</a>
		</nav>
	</div>
</header>

<slot />

<footer class="footer">
	<div class="wrap">
		<p>
			Built as a civic archive with moral clarity — for the people of Arkansas.
		</p>
	</div>
</footer>

<style>
	.top {
		position: sticky;
		top: 0;
		z-index: 50;
		backdrop-filter: blur(10px);
		background: rgba(255, 255, 255, 0.9);
		border-bottom: 1px solid rgba(0, 0, 0, 0.08);
	}

	.wrap {
		max-width: 980px;
		margin: 0 auto;
		padding: 0.9rem 1.25rem;
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: 1rem;
	}

	.brand {
		font-weight: 700;
		letter-spacing: -0.02em;
		text-decoration: none;
		color: inherit;
	}

	.nav {
		display: flex;
		gap: 1rem;
		flex-wrap: wrap;
	}

	.nav a {
		text-decoration: none;
		opacity: 0.85;
	}

	.nav a:hover {
		opacity: 1;
		text-decoration: underline;
	}

	.footer {
		border-top: 1px solid rgba(0, 0, 0, 0.08);
		margin-top: 3rem;
	}

	.footer p {
		margin: 0;
		padding: 1.25rem 0;
		opacity: 0.75;
	}
</style>
