import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params, url }) => {
  const locale = params.locale ?? 'en';
  const q = url.searchParams.get('q');

  const target = new URL('/__content', url.origin);
  target.searchParams.set('locale', locale);
  if (q) target.searchParams.set('q', q);

  return {
    status: 302,
    redirect: target.toString()
  };
};
