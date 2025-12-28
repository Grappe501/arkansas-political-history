import type { PageLoad } from './$types';
import { error } from '@sveltejs/kit';
import { getL2Topic } from '$lib/contracts/l2Topics';
import { getItemsByL2TopicSlug } from '$lib/content/archiveIndex';

type ArchiveItem = {
	section: string;
	slug: string;
	url: string;
	title: string;
	description: string;
	tags: string[];
	l2Topics?: string[];
	contentType?: string;
	learning?: {
		mode?: string;
		estimatedMinutes?: number | null;
		interactives?: string[];
	};
	date?: string;
	era?: string;
	place?: string;
	sourceUrl?: string;
	citation?: string;
	sourcePath?: string;
};

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
	const topicSlug = params.topic;

	const topic = getL2Topic(topicSlug);
	if (!topic) {
		throw error(404, `Unknown Level 2 topic: ${topicSlug}`);
	}

	const topicItems = (getItemsByL2TopicSlug(topic.slug) as ArchiveItem[]).sort((a, b) => {
		const ra = typeRank(a.contentType);
		const rb = typeRank(b.contentType);
		if (ra !== rb) return ra - rb;
		return (a.title ?? '').localeCompare(b.title ?? '');
	});

	const countsByType = topicItems.reduce<Record<string, number>>((acc, item) => {
		const k = (item.contentType ?? 'page').toLowerCase();
		acc[k] = (acc[k] ?? 0) + 1;
		return acc;
	}, {});

	return {
		locale,
		topic,
		items: topicItems,
		countsByType
	};
};
