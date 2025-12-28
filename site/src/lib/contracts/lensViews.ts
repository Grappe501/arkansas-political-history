import { getAllItems } from '$lib/content/archiveIndex';

export type LensViewSlug = 'geo' | 'demo' | 'political';

export type LensView = {
  slug: LensViewSlug;
  title: string;
  description: string;
  order: number;
  // tag namespaces this lens cares about
  namespaces: string[]; // e.g. ["place:", "geo:"]
};

export const LENS_VIEWS: LensView[] = [
  {
    slug: 'geo',
    title: 'Geography Lens',
    description: 'Counties • cities • districts • institutions on the ground.',
    order: 10,
    namespaces: ['place:', 'geo:', 'county:', 'city:', 'district:']
  },
  {
    slug: 'demo',
    title: 'Demographic Lens',
    description: 'Population composition • change over time • who is included/excluded.',
    order: 20,
    namespaces: ['demo:', 'race:', 'class:', 'age:', 'migration:', 'inclusion:']
  },
  {
    slug: 'political',
    title: 'Political Structure Lens',
    description: 'Legislature • judiciary • executive • local government • enforcement.',
    order: 30,
    namespaces: ['institution:', 'process:', 'courts', 'legislature', 'executive', 'local-government']
  }
];

export function getLensView(slug: string): LensView | null {
  const s = String(slug || '').trim() as LensViewSlug;
  return LENS_VIEWS.find((l) => l.slug === s) ?? null;
}

export function lensViewHref(locale: string, slug: string) {
  return `/${locale}/lenses/${slug}`;
}

/**
 * Items that belong to a lens view: any item containing any namespace prefix,
 * or for political lens, presence of core tokens like "courts" or "legislature".
 */
export function getItemsForLensView(slug: LensViewSlug) {
  const lens = getLensView(slug);
  if (!lens) return [];

  const items = getAllItems();
  const namespaces = lens.namespaces;

  return items.filter((it) => {
    const tags = it.tags ?? [];
    return tags.some((t) => {
      if (typeof t !== 'string') return false;

      // namespace prefix match
      if (namespaces.some((ns) => ns.endsWith(':') && t.startsWith(ns))) return true;

      // token match (for things like "courts", "legislature")
      if (namespaces.some((ns) => !ns.endsWith(':') && t.toLowerCase() === ns.toLowerCase())) return true;

      return false;
    });
  });
}

/**
 * Facets: top tags *within* the namespaces for that lens.
 * Returns tags sorted by frequency, most common first.
 */
export function getFacetTagsForLensView(slug: LensViewSlug, limit = 30) {
  const lens = getLensView(slug);
  if (!lens) return [];

  const namespaces = lens.namespaces;
  const items = getItemsForLensView(slug);

  const counts = new Map<string, number>();

  for (const it of items) {
    for (const tag of it.tags ?? []) {
      if (typeof tag !== 'string') continue;

      const isPrefix = namespaces.some((ns) => ns.endsWith(':') && tag.startsWith(ns));
      const isToken = namespaces.some((ns) => !ns.endsWith(':') && tag.toLowerCase() === ns.toLowerCase());

      if (!isPrefix && !isToken) continue;

      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }

  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([tag, count]) => ({ tag, count }));
}
