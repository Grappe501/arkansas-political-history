import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

const modules = import.meta.glob('/src/content/frameworks/**/*.md');

function pickKey(slugPath: string): string | null {
	const direct = `/src/content/frameworks/${slugPath}.md`;
	if (direct in modules) return direct;

	const asIndex = `/src/content/frameworks/${slugPath}/index.md`;
	if (asIndex in modules) return asIndex;

	return null;
}

export const load: PageLoad = async ({ params }) => {
	const slug = params.slug ?? '';
	const slugPath = Array.isArray(slug) ? slug.join('/') : slug;

	const key = pickKey(slugPath);
	if (!key) throw error(404, `Framework entry not found: ${slugPath}`);

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
