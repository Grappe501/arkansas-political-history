import { getL2TopicSlugsFromItems } from '$lib/content/archiveIndex';

export type L2Topic = {
  slug: string;
  title: string;
  description: string;
  order: number;
};

/**
 * Display metadata for known L2 topics.
 * The slug list itself is derived from archive-index.json via items[].l2Topics.
 *
 * As you add more L2 throughlines (counties/judiciary/legislature/church/etc),
 * just extend this map with the new slugs and their display copy.
 */
const L2_TOPIC_META: Record<string, Omit<L2Topic, 'slug'>> = {
  foundations: {
    title: 'Foundations',
    description:
      'Foundational constitutional eras, governance architecture, and the primary building blocks of Arkansas power.',
    order: 10
  },
  constitutions: {
    title: 'Constitutions',
    description:
      'How Arkansas rewrote power: constitutional eras, amendments, and the legal architecture that shaped institutions.',
    order: 20
  },
  'power-framework': {
    title: 'Power in Arkansas Framework',
    description:
      'A civic power literacy framework: how power flows, how it’s captured, and how communities reclaim it.',
    order: 30
  }
};

function titleizeSlug(slug: string) {
  return slug
    .split(/[-_/]+/g)
    .filter(Boolean)
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join(' ');
}

/**
 * Build the L2 topic list from the generated archive index.
 * If the index currently contains only 2 slugs, that’s what will render.
 * If an item references a new slug, it will appear automatically with a fallback title/desc.
 */
function buildTopics(): L2Topic[] {
  const slugs = getL2TopicSlugsFromItems();

  // If nothing is tagged yet, keep the dashboard alive with a minimal baseline.
  if (slugs.length === 0) {
    return [
      { slug: 'constitutions', ...L2_TOPIC_META.constitutions },
      { slug: 'power-framework', ...L2_TOPIC_META['power-framework'] }
    ];
  }

  return slugs.map((slug, i) => {
    const meta = L2_TOPIC_META[slug];

    if (meta) return { slug, ...meta };

    return {
      slug,
      title: titleizeSlug(slug),
      description: 'Explore this throughline across the archive.',
      order: 1000 + i
    };
  });
}

export const L2_TOPICS: L2Topic[] = buildTopics().sort((a, b) => a.order - b.order);

/**
 * Lookup helper used by /[locale]/l2/[topic] route.
 */
export function getL2Topic(slug: string): L2Topic | null {
  const key = String(slug || '').trim();
  if (!key) return null;
  return L2_TOPICS.find((t) => t.slug === key) ?? null;
}

export function l2TopicHref(locale: string, slug: string): string {
  return `/${locale}/l2/${slug}`;
}
