import type { PageLoad } from './$types';

// Generated at build time by site/scripts/build-content-index.mjs
import archiveIndex from '$lib/generated/archive-index.json';

type ArchiveItem = {
  section: string;
  slug: string;
  url: string;
  title: string;
  description: string;
  tags: string[];
  l2Topics?: string[];
  contentType?: string;
  date?: string;
  era?: string;
  place?: string;
};

function safeString(v: unknown): string {
  return typeof v === 'string' ? v : '';
}

function safeStringArray(v: unknown): string[] {
  return Array.isArray(v) ? v.filter((x) => typeof x === 'string') : [];
}

function normalizeItem(i: any): ArchiveItem {
  return {
    section: safeString(i.section),
    slug: safeString(i.slug),
    url: safeString(i.url),
    title: safeString(i.title),
    description: safeString(i.description),
    tags: safeStringArray(i.tags),
    l2Topics: safeStringArray(i.l2Topics),
    contentType: safeString(i.contentType),
    date: safeString(i.date),
    era: safeString(i.era),
    place: safeString(i.place)
  };
}

function uniq<T>(arr: T[]) {
  return Array.from(new Set(arr));
}

function includesCI(hay: string, needle: string) {
  return hay.toLowerCase().includes(needle.toLowerCase());
}

export const load: PageLoad = async ({ params, url }) => {
  const locale = params.locale ?? 'en';

  const q = url.searchParams.get('q') ?? '';
  const l2 = url.searchParams.get('l2') ?? '';
  const placeTag = url.searchParams.get('place') ?? ''; // exact tag match
  const section = url.searchParams.get('section') ?? '';
  const type = url.searchParams.get('type') ?? '';

  const rawItems = (archiveIndex as any)?.items ?? [];
  const items: ArchiveItem[] = Array.isArray(rawItems) ? rawItems.map(normalizeItem) : [];

  // “Place-like” tags are what power users will standardize over time.
  // Supports: place:* and geo:* now; later we can add richer joining.
  const allPlaceTags = uniq(
    items
      .flatMap((i) => i.tags ?? [])
      .filter((t) => /^place:|^geo:/i.test(t))
      .sort((a, b) => a.localeCompare(b))
  );

  let filtered = items.slice();

  if (l2) filtered = filtered.filter((i) => (i.l2Topics ?? []).includes(l2));
  if (section) filtered = filtered.filter((i) => i.section === section);
  if (type) filtered = filtered.filter((i) => (i.contentType ?? '').toLowerCase() === type.toLowerCase());
  if (placeTag) filtered = filtered.filter((i) => (i.tags ?? []).includes(placeTag));

  if (q.trim()) {
    filtered = filtered.filter((i) => {
      const blob = `${i.title} ${i.description} ${i.slug} ${(i.tags ?? []).join(' ')}`;
      return includesCI(blob, q.trim());
    });
  }

  // Simple predictable ordering for now
  filtered.sort((a, b) => (a.title ?? '').localeCompare(b.title ?? ''));

  const sections = uniq(items.map((i) => i.section).filter(Boolean)).sort((a, b) => a.localeCompare(b));
  const types = uniq(items.map((i) => (i.contentType ?? 'page').toLowerCase()).filter(Boolean)).sort((a, b) =>
    a.localeCompare(b)
  );

  return {
    locale,
    q,
    l2,
    placeTag,
    section,
    type,
    placeTags: allPlaceTags,
    sections,
    types,
    items: filtered
  };
};
