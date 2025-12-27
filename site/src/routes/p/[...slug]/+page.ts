import { error } from '@sveltejs/kit';

type MdModule = {
	default: unknown; // mdsvex component
	metadata?: Record<string, any>;
};

function normalizeSlug(input: unknown) {
	const s = Array.isArray(input) ? input.join('/') : String(input ?? '');
	return s.trim().replace(/^\/+/, '').replace(/\/+$/, '');
}

function slugFromModulePath(p: string) {
	return p.replace(/^\/src\/content\/pages\//, '').replace(/\.md$/, '');
}

export async function load({ params }) {
	const slug = normalizeSlug(params.slug);

	const modules = import.meta.glob<MdModule>('/src/content/pages/**/*.md');

	let matchPath: string | null = null;
	for (const p of Object.keys(modules)) {
		if (slugFromModulePath(p) === slug) {
			matchPath = p;
			break;
		}
	}

	if (!matchPath) {
		throw error(404, `Page not found: /p/${slug}`);
	}

	const mod = await modules[matchPath]();
	const meta = mod.metadata ?? {};

	return {
		slug,
		component: mod.default,
		meta
	};
}
