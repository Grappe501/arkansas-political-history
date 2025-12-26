import fs from 'node:fs';
import path from 'node:path';
import fg from 'fast-glob';
import matter from 'gray-matter';

const SITE_ROOT = process.cwd();
const CONTENT_ROOT = path.join(SITE_ROOT, 'src', 'content');

const OUT_DIR = path.join(SITE_ROOT, 'src', 'lib', 'generated');
const OUT_FILE = path.join(OUT_DIR, 'archive-index.json');

function ensureDir(p) {
	fs.mkdirSync(p, { recursive: true });
}

function toUrlPath(p) {
	return p.split(path.sep).join('/');
}

function normalizeTags(v) {
	if (Array.isArray(v)) return v.filter((t) => typeof t === 'string');
	if (typeof v === 'string') return [v];
	return [];
}

function safeReadUtf8(file) {
	// If any weird bytes exist, replace invalid sequences safely.
	const buf = fs.readFileSync(file);
	return buf.toString('utf8');
}

function indexFolder(section, folderRel) {
	const folderAbs = path.join(CONTENT_ROOT, folderRel);
	if (!fs.existsSync(folderAbs)) {
		fs.mkdirSync(folderAbs, { recursive: true });
		return [];
	}

	const files = fg.sync(['**/*.md'], { cwd: folderAbs, dot: false });

	return files.map((rel) => {
		const full = path.join(folderAbs, rel);
		const raw = safeReadUtf8(full);
		const parsed = matter(raw);
		const meta = parsed.data ?? {};

		const relNoExt = rel.replace(/\.md$/i, '');
		const slugPath = toUrlPath(relNoExt);

		let url = '';
		switch (section) {
			case 'pages':
				url = `/p/${slugPath}`;
				break;
			case 'timelines':
				url = `/timeline/${slugPath}`;
				break;
			case 'frameworks':
				url = `/power/${slugPath}`;
				break;
			case 'constitutions':
				url = `/constitutions/${slugPath}`;
				break;
			case 'legislative':
				url = `/legislative/${slugPath}`;
				break;
			case 'sources':
				url = `/sources/${slugPath}`;
				break;
			default:
				url = `/${section}/${slugPath}`;
		}

		const title = typeof meta.title === 'string' ? meta.title : slugPath;
		const description = typeof meta.description === 'string' ? meta.description : '';
		const tags = normalizeTags(meta.tags);

		const date = typeof meta.date === 'string' ? meta.date : '';
		const era = typeof meta.era === 'string' ? meta.era : '';
		const place = typeof meta.place === 'string' ? meta.place : '';

		return {
			section,
			slug: slugPath,
			url,
			title,
			description,
			tags,
			date,
			era,
			place
		};
	});
}

function main() {
	ensureDir(OUT_DIR);

	const sections = [
		{ section: 'pages', folderRel: 'pages' },
		{ section: 'timelines', folderRel: 'timelines' },
		{ section: 'frameworks', folderRel: 'frameworks' },
		{ section: 'constitutions', folderRel: 'constitutions' },
		{ section: 'legislative', folderRel: 'legislative-process' },
		{ section: 'sources', folderRel: 'sources' }
	];

	const items = sections.flatMap((s) => indexFolder(s.section, s.folderRel));

	const tagMap = new Map();
	for (const item of items) {
		for (const tag of item.tags) {
			if (!tagMap.has(tag)) tagMap.set(tag, []);
			tagMap.get(tag).push(item.url);
		}
	}

	const tags = Array.from(tagMap.entries())
		.map(([tag, urls]) => ({
			tag,
			count: urls.length,
			urls: urls.sort()
		}))
		.sort((a, b) => a.tag.localeCompare(b.tag));

	const payload = {
		generatedAt: new Date().toISOString(),
		count: items.length,
		items: items.sort((a, b) => a.url.localeCompare(b.url)),
		tags
	};

	fs.writeFileSync(OUT_FILE, JSON.stringify(payload, null, 2), 'utf8');
	console.log(`[build-content-index] Wrote: ${OUT_FILE}`);
	console.log(`[build-content-index] Items indexed: ${items.length}`);
	console.log(`[build-content-index] Tags indexed: ${tags.length}`);
}

main();
