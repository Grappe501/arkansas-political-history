import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

// Compile-time list of markdown modules under /src/content/pages
const modules = import.meta.glob('/src/content/pages/**/*.md');

function pickKey(slugPath: string): string | null {
	// Try exact file
	const direct = `/src/content/pages/${slugPath}.md`;
	if (direct in modules) return direct;

	// Try index.md for folder slugs
	const asIndex = `/src/content/pages/${slugPath}/index.md`;
	if (asIndex in modules) return asIndex;

	return null;
}

export const load: PageLoad = async ({ params }) => {
	const slug = params.slug ?? '';
	const slugPath = Array.isArray(slug) ? slug.join('/') : slug;

	const key = pickKey(slugPath);
	if (!key) throw error(404, `Page not found: ${slugPath}`);

	const mod = (await modules[key]()) as {
		default: unknown;
		metadata?: Record<string, unknown>;
	};

	return {
		component: mod.default,
		metadata: mod.metadata ?? {},
		slug: slugPath
	};
};
