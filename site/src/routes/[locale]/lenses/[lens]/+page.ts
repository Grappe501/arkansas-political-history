import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import { getLensView, getItemsForLensView, getFacetTagsForLensView } from '$lib/contracts/lensViews';

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

export const load: PageLoad = async ({ params }) => {
  const locale = params.locale ?? 'en';
  const slug = params.lens;

  const lens = getLensView(slug);
  if (!lens) throw error(404, `Unknown lens view: ${slug}`);

  const items = getItemsForLensView(lens.slug)
    .slice()
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

  const facets = getFacetTagsForLensView(lens.slug, 36);

  return { locale, lens, items, countsByType, facets };
};
