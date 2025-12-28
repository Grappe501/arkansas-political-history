/**
 * Level 2 Topic Contracts
 * Single source of truth for Level 2 navigation + routing.
 */

export type L2TopicSlug =
  | 'foundations'
  | 'power'
  | 'money'
  | 'process'
  | 'people'
  | 'cases'
  | 'toolkit'
  | 'sources'
  | 'trackers'
  | 'about';

export type L2TopicContract = {
  slug: L2TopicSlug;
  title: string;
  description: string;
  order: number;
};

export const L2_TOPICS: ReadonlyArray<L2TopicContract> = Object.freeze([
  {
    slug: 'foundations',
    title: 'Foundations',
    description: 'Core civic literacy: what government is, why it works, and how power is supposed to flow.',
    order: 10
  },
  {
    slug: 'power',
    title: 'Power Map',
    description: 'How influence actually moves in Arkansas—institutions, gatekeepers, and leverage points.',
    order: 20
  },
  {
    slug: 'money',
    title: 'Money & Influence',
    description: 'Money flows, incentives, procurement, lobbying, and the mechanisms that convert dollars into policy.',
    order: 30
  },
  {
    slug: 'process',
    title: 'Rules & Process',
    description: 'The procedural playbook: committees, rules, elections, and how outcomes get decided.',
    order: 40
  },
  {
    slug: 'people',
    title: 'People & Networks',
    description: 'Power is social: the networks, alliances, and reputational systems that run a state.',
    order: 50
  },
  {
    slug: 'cases',
    title: 'Case Files',
    description: 'Real-world examples showing the power system in motion, with sources and receipts.',
    order: 60
  },
  {
    slug: 'toolkit',
    title: 'Civic Toolkit',
    description: 'Practical tools: how to show up, organize, file requests, testify, petition, and run.',
    order: 70
  },
  {
    slug: 'sources',
    title: 'Sources & Provenance',
    description: 'How we know what we know: evidence standards, citations, and a trail you can verify.',
    order: 80
  },
  {
    slug: 'trackers',
    title: 'Trackers',
    description: 'Dashboards and monitoring systems for legislation, money, power, and accountability.',
    order: 90
  },
  {
    slug: 'about',
    title: 'About & Governance',
    description: 'Mission, standards, editorial governance, and how the project stays accountable to people.',
    order: 100
  }
]);

export function getL2Topic(slug: string): L2TopicContract | undefined {
  return (L2_TOPICS as L2TopicContract[]).find((t) => t.slug === slug);
}

export function l2TopicHref(locale: string, slug: string): string {
  const safeLocale = locale || 'en';
  return `/${safeLocale}/l2/${slug}`;
}
