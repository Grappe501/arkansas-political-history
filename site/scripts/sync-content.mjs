import fs from 'node:fs';
import path from 'node:path';

const SITE_ROOT = process.cwd(); // Netlify base dir = /opt/build/repo/site
const REPO_ROOT = path.resolve(SITE_ROOT, '..');

const SOURCE = path.join(REPO_ROOT, 'content');
const DEST = path.join(SITE_ROOT, 'src', 'content');

function ensureDir(p) {
	fs.mkdirSync(p, { recursive: true });
}

function copyDir(src, dest) {
	ensureDir(dest);

	fs.cpSync(src, dest, {
		recursive: true,
		force: true,
		filter: (srcPath) => {
			const base = path.basename(srcPath).toLowerCase();
			if (base === '.ds_store' || base === 'thumbs.db') return false;
			if (base.endsWith('.tmp')) return false;
			return true;
		}
	});
}

function walkFiles(dir, files = []) {
	const entries = fs.readdirSync(dir, { withFileTypes: true });
	for (const e of entries) {
		const full = path.join(dir, e.name);
		if (e.isDirectory()) walkFiles(full, files);
		else files.push(full);
	}
	return files;
}

function normalizeUnicodePunctuation(s) {
	// --- Unicode smart quotes ---
	s = s.replace(/\u201C|\u201D/g, '"');
	s = s.replace(/\u2018|\u2019/g, "'");

	// --- CP1252 “control” quote bytes that sometimes survive as U+009x ---
	// These frequently show up from DOCX/HTML exports and render like curly quotes.
	s = s.replace(/\u0091|\u0092/g, "'"); // ‘ ’ (cp1252 0x91 0x92)
	s = s.replace(/\u0093|\u0094/g, '"'); // “ ” (cp1252 0x93 0x94)

	// Some other common cp1252 oddities that can appear
	s = s.replace(/\u0096|\u0097/g, '-'); // en/em dash variants
	s = s.replace(/\u0085/g, '...'); // ellipsis variant

	// en/em dashes -> hyphen
	s = s.replace(/\u2013|\u2014/g, '-');

	// ellipsis
	s = s.replace(/\u2026/g, '...');

	// non-breaking spaces -> normal spaces
	s = s.replace(/\u00A0/g, ' ');

	return s;
}

function splitFrontmatter(md) {
	const lines = md.split(/\r?\n/);
	if (lines.length < 3) return { fm: '', body: md };
	if (lines[0].trim() !== '---') return { fm: '', body: md };

	let end = -1;
	for (let i = 1; i < lines.length; i++) {
		if (lines[i].trim() === '---') {
			end = i;
			break;
		}
	}
	if (end === -1) return { fm: '', body: md };

	const fm = lines.slice(0, end + 1).join('\n');
	const body = lines.slice(end + 1).join('\n');
	return { fm, body };
}

function looksLikeJsonBody(lines) {
	let colonCount = 0;
	let keyLike = 0;

	for (const ln of lines) {
		const t = ln.trim();
		if (!t) continue;
		if (t.includes(':')) colonCount++;
		if (/^["'][^"']+["']\s*:/.test(t)) keyLike++;
	}

	return colonCount >= 2 && keyLike >= 1;
}

function fenceBareJsonBlocks(markdown) {
	const lines = markdown.split(/\r?\n/);
	let inFence = false;

	const out = [];
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		const trimmed = line.trim();

		if (trimmed.startsWith('```')) {
			inFence = !inFence;
			out.push(line);
			continue;
		}

		if (!inFence && trimmed === '{') {
			const maxLookahead = 80;
			let foundClose = -1;

			for (let j = i + 1; j < lines.length && j <= i + maxLookahead; j++) {
				if (lines[j].trim().startsWith('```')) break;
				if (lines[j].trim() === '}') {
					foundClose = j;
					break;
				}
			}

			if (foundClose !== -1) {
				const block = lines.slice(i, foundClose + 1);
				if (looksLikeJsonBody(block.slice(1, -1))) {
					out.push('```json');
					for (const bl of block) out.push(bl);
					out.push('```');
					i = foundClose;
					continue;
				}
			}
		}

		out.push(line);
	}

	return out.join('\n');
}

function escapePlaceholderTagsOutsideCode(markdown) {
	const placeholders = ['slug', 'tag', 'category', 'routeBase', 'routebase', 'id', 'url'];

	const lines = markdown.split(/\r?\n/);
	let inFence = false;

	const out = lines.map((line) => {
		const trimmed = line.trim();
		if (trimmed.startsWith('```')) {
			inFence = !inFence;
			return line;
		}
		if (inFence) return line;

		let s = line;
		for (const name of placeholders) {
			s = s.split(`<${name}>`).join(`&lt;${name}&gt;`);
			s = s.split(`</${name}>`).join(`&lt;/${name}&gt;`);
		}
		return s;
	});

	return out.join('\n');
}

function escapeSvelteBracesEverywhere(markdown) {
	// Convert braces to Svelte-safe literal expressions
	// { -> {'{'}  and  } -> {'}'}
	return markdown.replace(/\{/g, "{'{'}").replace(/\}/g, "{'}'}");
}

function sanitizeMarkdown(markdown) {
	const { fm, body } = splitFrontmatter(markdown);

	let s = body;

	// Normalize hard (handles both U+2019 and U+0092 style junk)
	s = normalizeUnicodePunctuation(s);

	// Fence bare JSON-looking blocks
	s = fenceBareJsonBlocks(s);
	s = normalizeUnicodePunctuation(s);

	// Escape placeholder tags
	s = escapePlaceholderTagsOutsideCode(s);
	s = normalizeUnicodePunctuation(s);

	// IMPORTANT: normalize one more time right before brace escaping
	// so we never end up with {’} patterns inside mdsvex output.
	s = normalizeUnicodePunctuation(s);

	// Escape braces last
	s = escapeSvelteBracesEverywhere(s);

	// Final normalize pass (belt + suspenders)
	s = normalizeUnicodePunctuation(s);

	return fm ? `${fm}\n${s.replace(/^\n+/, '')}` : s;
}

/**
 * Detect content patterns likely to break mdsvex/Svelte compilation
 * even after sanitization. If matched, we will delete the file entirely.
 *
 * This is intentionally strict: if a doc is "instructional" and contains
 * artifacts like <p>...</p> wrappers, token spans, or templating junk,
 * it's safer to drop it from runtime content and re-add later as docs.
 */
function hasMdsvexBreakerPatterns(text) {
	// 1) Curly quotes that survive as unicode (should usually be normalized, but catch anyway)
	const badQuotes = /[\u2018\u2019\u201C\u201D]/;

	// 2) CP1252 control-range characters that often cause weird parsing/encoding issues
	const cp1252Controls = /[\u0080-\u009F]/;

	// 3) Common DOCX/HTML export wrappers that turn markdown into HTML soup
	const htmlSoup = /<p>|<\/p>|<span\b[^>]*class="token"[^>]*>|<\/span>/i;

	// 4) Known mdsvex/Svelte breaker: literal "{’}’}" or similar brace+quote artifacts
	const braceQuoteArtifact = /\{\s*[’“”‘']\s*\}|\{[’“”‘']\}|\{[’“”‘'][^}]*\}/;

	// 5) Suspicious leftover HTML entities for braces in code contexts (a sign of mangled content)
	const mangledBracesEntities = /&#123;|&#125;/;

	return (
		badQuotes.test(text) ||
		cp1252Controls.test(text) ||
		htmlSoup.test(text) ||
		braceQuoteArtifact.test(text) ||
		mangledBracesEntities.test(text)
	);
}

function sanitizeAndDeleteBadMarkdownFilesInDir(dir) {
	const files = walkFiles(dir);
	let sanitized = 0;
	let deleted = 0;

	const deletedFiles = [];

	for (const file of files) {
		if (!file.toLowerCase().endsWith('.md')) continue;

		const raw = fs.readFileSync(file, 'utf8');
		const cleaned = sanitizeMarkdown(raw);

		// Write sanitized content first (so we benefit from normalization)
		if (cleaned !== raw) {
			fs.writeFileSync(file, cleaned, 'utf8');
			sanitized++;
		}

		// Re-read after sanitize, then decide if it's still too risky
		const post = fs.readFileSync(file, 'utf8');

		if (hasMdsvexBreakerPatterns(post)) {
			fs.rmSync(file, { force: true });
			deleted++;
			deletedFiles.push(file);
		}
	}

	console.log(`[sync-content] Sanitized markdown files: ${sanitized}`);
	console.log(`[sync-content] Deleted risky markdown files: ${deleted}`);

	if (deletedFiles.length) {
		console.log('[sync-content] Deleted files:');
		for (const f of deletedFiles) console.log(`  - ${f}`);
	}
}

function main() {
	if (!fs.existsSync(SOURCE)) {
		console.log(`[sync-content] No /content folder found at: ${SOURCE}`);
		console.log('[sync-content] Creating empty content structure...');
		ensureDir(path.join(SOURCE, 'pages'));
		ensureDir(path.join(SOURCE, 'timelines'));
		ensureDir(path.join(SOURCE, 'frameworks'));
		ensureDir(path.join(SOURCE, 'constitutions'));
		ensureDir(path.join(SOURCE, 'legislative-process'));
		ensureDir(path.join(SOURCE, 'sources'));
	}

	console.log(`[sync-content] Syncing content:`);
	console.log(`  from: ${SOURCE}`);
	console.log(`  to:   ${DEST}`);

	if (fs.existsSync(DEST)) {
		fs.rmSync(DEST, { recursive: true, force: true });
	}

	copyDir(SOURCE, DEST);

	// sanitize, then delete anything that still looks like it will break mdsvex
	sanitizeAndDeleteBadMarkdownFilesInDir(DEST);

	console.log('[sync-content] Done.');
}

main();
