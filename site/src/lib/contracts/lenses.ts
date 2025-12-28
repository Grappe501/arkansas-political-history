import { getAllItems } from '$lib/content/archiveIndex';

export type Lens = {
  slug: string;
  title: string;
  description: string;
  order: number;
};

const LENS_META: Record<string, Omit<Lens, 'slug'>> = {
  // --- Geo lenses (examples; you can adjust anytime) ---
  delta: {
    title: 'Delta Lens',
    description:
      'Read the archive through the Delta: plantation economy, labor control, migration, suppression, and long-run institutional capture.',
    order: 10
  },
  ozarks: {
    title: 'Ozarks Lens',
    description:
      'Read the archive through the Ozarks: land, extraction, church networks, local control, and cultural power.',
    order: 20
  },
  river: {
    title: 'River Valley Lens',
    description:
      'Read the archive through the River Valley: industry, logistics corridors, labor, and shifting power coalitions.',
    order: 30
  },
  littlerockmetro: {
    title: 'Little Rock Metro Lens',
    description:
      'Read the archive through the state capital region: bureaucracy, courts, administrative power, and elite networks.',
    order: 40
  },

  // --- Demographic/political structure lenses ---
  blackpolitics: {
    title: 'Black Politics Lens',
    description:
      'Track governance and power as experienced by Black Arkansans: rights, backlash, enforcement gaps, and institutional workarounds.',
    order: 110
  },
  partyrealignment: {
    title: 'Party Realignment Lens',
    description:
      'Follow coalition shifts over time: elites, institutions, and how power reorganizes when party labels change.',
    order: 120
  },

  // --- Institution lenses ---
  courts: {
    title: 'Courts Lens',
    description:
      'Filter for judicial gatekeeping, enforcement, procedural control, and the courts as power brokers.',
    order: 210
  },
  legislature: {
    title: 'Legislature Lens',
    description:
      'Filter for legislative procedure, agenda control, committee choke points, and rule-based domination.',
    order: 220
  },
  church: {
    title: 'Church Lens',
    description:
      'Filter for faith institutions and political theology: networks, mobilization, moral authority, and legitimacy production.',
    order: 230
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
 * Extract unique lens slugs from tags like: "lens:<slug>"
 */
export function getLensSlugsFromItems(): string[] {
  const set = new Set<string>();

  for (const item of getAllItems()) {
    const tags = item.tags ?? [];
    for (const t of tags) {
      if (typeof t !== 'string') continue;
      if (!t.startsWith('lens:')) continue;

      const slug = t.slice('lens:'.length).trim();
      if (slug) set.add(slug);
    }
  }

  return [...set].sort((a, b) => a.localeCompare(b));
}

export function buildLenses(): Lens[] {
  const slugs = getLensSlugsFromItems();

  // keep the dashboard alive even before content is tagged
  if (slugs.length === 0) {
    const defaults = ['delta', 'ozarks', 'littlerockmetro', 'courts', 'legislature'];
    return defaults
      .map((slug, i) => {
        const meta = LENS_META[slug];
        if (meta) return { slug, ...meta };
        return {
          slug,
          title: titleizeSlug(slug),
          description: 'Explore this lens across the archive.',
          order: 1000 + i
        };
      })
      .sort((a, b) => a.order - b.order);
  }

  return slugs
    .map((slug, i) => {
      const meta = LENS_META[slug];
      if (meta) return { slug, ...meta };

      return {
        slug,
        title: titleizeSlug(slug),
        description: 'Explore this lens across the archive.',
        order: 1000 + i
      };
    })
    .sort((a, b) => a.order - b.order);
}

export const LENSES: Lens[] = buildLenses();

export function getLens(slug: string): Lens | null {
  const key = String(slug || '').trim();
  if (!key) return null;
  return LENSES.find((l) => l.slug === key) ?? null;
}

export function lensHref(locale: string, slug: string) {
  return `/${locale}/lenses/${slug}`;
}
