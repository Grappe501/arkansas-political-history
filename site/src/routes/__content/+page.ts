import type { PageLoad } from './$types';
import { ARCHIVE_INDEX } from '$lib/content/archiveIndex';

export const load: PageLoad = async ({ url }) => {
  const locale = url.searchParams.get('locale') ?? 'en';
  const q = (url.searchParams.get('q') ?? '').trim();

  // Lightweight filtering in load so SSR renders useful output immediately.
  // (We still do client-side refinement in the Svelte page as needed.)
  const items = ARCHIVE_INDEX.items ?? [];

  const filtered =
    q.length === 0
      ? items
      : items.filter((it) => {
          const hay = [
            it.title,
            it.description,
            it.section,
            it.slug,
            it.url,
            (it.tags ?? []).join(' ')
          ]
            .join(' ')
            .toLowerCase();

          return hay.includes(q.toLowerCase());
        });

  return {
    generatedAt: ARCHIVE_INDEX.generatedAt,
    contentRoot: ARCHIVE_INDEX.contentRoot,
    count: ARCHIVE_INDEX.count,
    locale,
    q,
    items: filtered
  };
};
