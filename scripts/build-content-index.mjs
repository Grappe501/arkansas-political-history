import fs from 'node:fs';
import path from 'node:path';
import fg from 'fast-glob';
import matter from 'gray-matter';

const ROOT = process.cwd();
const CONTENT_ROOT = path.join(ROOT, 'site', 'src', 'content');
const PAGES_ROOT = path.join(CONTENT_ROOT, 'pages');
const OUT_DIR = path.join(ROOT, 'site', 'src', 'lib', 'generated');
const OUT_FILE = path.join(OUT_DIR, 'content-index.json');

function ensureDir(p) {
	fs.mkdirSync(p, { recursive: true });
}

function normalizeSlug(relPathNoExt) {
	// Windows path -> URL path
	return relPathNoExt.split(path.sep).join('/');
}

function main() {
	ensureDir(OUT_DIR);

	if (!fs.existsSync(PAGES_ROOT)) {
		console.log(`[build-content-index] No pages folder found: ${PAGES_ROOT}`);
		console.log('[build-content-index] Creating it.');
		fs.mkdirSync(PAGES_ROOT, { recursive: true });
	}

	const patterns = ['**/*.md'];
	const files = fg.sync(patterns, { cwd: PAGES_ROOT, dot: false });

	const items = files
		.map((rel) => {
			const full = path.join(PAGES_ROOT, rel);
			const raw = fs.readFileSync(full, 'utf8');
			const parsed = matter(raw);

			const relNoExt = rel.replace(/\.md$/i, '');
			const slug = normalizeSlug(relNoExt);

			const meta = parsed.data ?? {};
			const title = typeof meta.title === 'string' ? meta.title : slug;
			const description = typeof meta.description === 'string' ? meta.description : '';
			const tags = Array.isArray(meta.tags) ? meta.tags : [];

			return {
				slug,
				title,
				description,
				tags
			};
		})
		.sort((a, b) => a.slug.localeCompare(b.slug));

	const payload = {
		generatedAt: new Date().toISOString(),
		count: items.length,
		items
	};

	fs.writeFileSync(OUT_FILE, JSON.stringify(payload, null, 2), 'utf8');
	console.log(`[build-content-index] Wrote: ${OUT_FILE}`);
	console.log(`[build-content-index] Pages indexed: ${items.length}`);
}

main();
