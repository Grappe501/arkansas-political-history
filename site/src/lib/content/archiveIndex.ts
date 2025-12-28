import archiveIndexJson from '$lib/generated/archive-index.json';

export type ArchiveLearning = {
  mode?: string;
  estimatedMinutes?: number | null;
  interactives?: string[];
};

export type ArchiveItem = {
  section: string;
  slug: string;
  url: string;
  title: string;
  description: string;
  tags: string[];
  l2Topics?: string[];
  contentType?: string;
  learning?: ArchiveLearning;
  date?: string;
  era?: string;
  place?: string;
  sourceUrl?: string;
  citation?: string;
  sourcePath?: string;
};

export type ArchiveIndex = {
  generatedAt: string;
  contentRoot: string;
  count: number;
  items: ArchiveItem[];
};

export const ARCHIVE_INDEX = archiveIndexJson as unknown as ArchiveIndex;

export function getAllItems(): ArchiveItem[] {
  return ARCHIVE_INDEX.items ?? [];
}

/**
 * Unique list of L2 topic slugs referenced by content items.
 * This is the most reliable source right now because the generated JSON
 * may or may not include a top-level `l2Topics` array.
 */
export function getL2TopicSlugsFromItems(): string[] {
  const set = new Set<string>();

  for (const item of getAllItems()) {
    const topics = item.l2Topics ?? [];
    for (const t of topics) {
      const slug = String(t || '').trim();
      if (slug) set.add(slug);
    }
  }

  return [...set].sort((a, b) => a.localeCompare(b));
}

/**
 * Convenience: get all items for a given L2 topic slug.
 */
export function getItemsByL2TopicSlug(slug: string): ArchiveItem[] {
  const target = String(slug || '').trim();
  if (!target) return [];

  return getAllItems().filter((it) => (it.l2Topics ?? []).includes(target));
}
