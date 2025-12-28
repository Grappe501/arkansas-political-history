import type { PageLoad } from './$types';
import { LENSES } from '$lib/contracts/lenses';
import { getAllItems } from '$lib/content/archiveIndex';

export const load: PageLoad = async ({ params }) => {
  const locale = params.locale ?? 'en';

  const items = getAllItems();

  const countsByLens = LENSES.reduce<Record<string, number>>((acc, l) => {
    const tag = `lens:${l.slug}`;
    const count = items.filter((it) => (it.tags ?? []).includes(tag)).length;
    acc[l.slug] = count;
    return acc;
  }, {});

  return {
    locale,
    lenses: LENSES,
    countsByLens
  };
};
