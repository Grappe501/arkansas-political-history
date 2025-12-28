import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import { getAllItems } from '$lib/content/archiveIndex';

type Lens = {
	slug: string;
	title: string;
	description: string;
	order: number;
	namespaces: string[]; // tag prefixes like ["geo:", "place:", "county:"]
};

const LENSES: Record<string, Lens> = {
	geo: {
		slug: 'geo',
		title: 'Geography Lens',
		description: 'Counties • cities • districts • institutions on the ground.',
		order: 10,
		namespaces: ['geo:', 'place:', 'county:', 'city:', 'district:', 'fips:']
	},
	demo: {
		slug: 'demo',
		title: 'Demographic Lens',
		description: 'Population composition • change over time • who is included/excluded.',
		order: 20,
		namespaces: ['demo:', 'race:', 'income:', 'class:', 'age:', 'pop:', 'urban-rural:']
	},
	political: {
		slug: 'political',
		title: 'Political Structure Lens',
		description: 'Legislature • judiciary • executive • local government • enforcement.',
		order: 30,
		namespaces: ['inst:', 'mechanism:', 'branch:', 'office:', 'agency:', 'committee:']
	}
};

const TYPE_ORDER: Record<string, number> = {
	lesson: 10,
	explainer: 20,
	framework: 30,
	case: 40,
	timeline: 50,
	source: 60,
	reference: 70,
	page: 80
};

function typeRank(t?: string) {
	const key = (t ?? '').toLowerCase();
	return TYPE_ORDER[key] ?? 999;
}

function hasNamespacedTag(tags: string[], namespaces: string[]) {
	const t = tags ?? [];
	return t.some((tag) => namespaces.some((ns) => tag.toLowerCase().startsWith(ns.toLowerCase())));
}

function facetCounts(items: { tags: string[] }[], namespaces: string[]) {
	const map = new Map<string, number>();

	for (const it of items) {
		for (const tag of it.tags ?? []) {
			if (namespaces.some((ns) => tag.toLowerCase().startsWith(ns.toLowerCase()))) {
				map.set(tag, (map.get(tag) ?? 0) + 1);
			}
		}
	}

	return [...map.entries()]
		.map(([tag, count]) => ({ tag, count }))
		.sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag))
		.slice(0, 40);
}

export const load: PageLoad = ({ params }) => {
	const locale = params.locale ?? 'en';

	// Route folder must be [lens] for this to exist:
	const lensSlug = (params as Record<string, string | undefined>).lens;
	if (!lensSlug) throw error(404, 'Missing lens slug');

	const lens = LENSES[lensSlug];
	if (!lens) throw error(404, `Unknown lens: ${lensSlug}`);

	const all = getAllItems();

	// Filter to items that have at least one tag in the lens namespaces
	const items = all
		.filter((it) => hasNamespacedTag(it.tags ?? [], lens.namespaces))
		.sort((a, b) => {
			const ra = typeRank(a.contentType);
			const rb = typeRank(b.contentType);
			if (ra !== rb) return ra - rb;
			return (a.title ?? '').localeCompare(b.title ?? '');
		});

	const countsByType = items.reduce<Record<string, number>>((acc, item) => {
		const k = (item.contentType ?? 'page').toLowerCase();
		acc[k] = (acc[k] ?? 0) + 1;
		return acc;
	}, {});

	const facets = facetCounts(items, lens.namespaces);

	return {
		locale,
		lens,
		items,
		countsByType,
		facets
	};
};
