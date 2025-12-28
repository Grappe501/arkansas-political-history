import fs from 'node:fs';
import path from 'node:path';
import fg from 'fast-glob';
import matter from 'gray-matter';

const ROOT = process.cwd();

/**
 * We want to index the repository-level /content folder:
 *   C:\...\Arkansas_Political_History\content
 *
 * This script lives in /site/scripts and is executed from /site,
 * so repo root is typically: path.join(ROOT, '..')
 *
 * We keep this robust in case someone runs it from repo root.
 */
function resolveRepoRoot() {
  // If running inside /site, repo root is parent.
  if (path.basename(ROOT).toLowerCase() === 'site') return path.join(ROOT, '..');
  // Otherwise assume current working directory is repo root.
  return ROOT;
}

function resolveContentRoot() {
  // Allow explicit override for CI or custom layouts
  const envRoot = process.env.CONTENT_ROOT ? process.env.CONTENT_ROOT.trim() : '';
  if (envRoot) {
    const abs = path.isAbsolute(envRoot) ? envRoot : path.resolve(ROOT, envRoot);
    if (!fs.existsSync(abs)) {
      throw new Error(`[build-content-index] CONTENT_ROOT override does not exist: ${abs}`);
    }
    return abs;
  }

  const repoRoot = resolveRepoRoot();
  const p = path.join(repoRoot, 'content');

  if (!fs.existsSync(p)) {
    throw new Error(
      `[build-content-index] Could not find repo content folder at: ${p}\n` +
        `Expected: <repoRoot>/content\n` +
        `Current working directory: ${ROOT}`
    );
  }

  return p;
}

function resolveOutDir() {
  // Always write into the site app generated folder.
  // If running from repo root, this still resolves correctly.
  const repoRoot = resolveRepoRoot();
  const siteRoot = path.join(repoRoot, 'site');
  const out = path.join(siteRoot, 'src', 'lib', 'generated');
  return out;
}

const CONTENT_ROOT = resolveContentRoot();
const OUT_DIR = resolveOutDir();
const OUT_FILE = path.join(OUT_DIR, 'archive-index.json');

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function toUrlPath(p) {
  return p.split(path.sep).join('/');
}

function normalizeStringArray(v) {
  if (Array.isArray(v))
    return v
      .filter((t) => typeof t === 'string' && t.trim().length > 0)
      .map((t) => t.trim());
  if (typeof v === 'string' && v.trim().length > 0) return [v.trim()];
  return [];
}

function normalizeTags(v) {
  return normalizeStringArray(v);
}

/**
 * L2 topic slugs:
 * - accept string or array
 * - normalize to lowercase trimmed strings
 */
function normalizeL2Topics(v) {
  const arr = normalizeStringArray(v);
  return arr.map((s) => s.toLowerCase());
}

/**
 * ContentType contract:
 * - used by dashboards and learning renderers to decide display + behavior
 * - tolerant default: infer from section, but allow override in frontmatter
 */
function normalizeContentType(meta, section) {
  const raw = typeof meta.contentType === 'string' ? meta.contentType.trim() : '';
  if (raw) return raw;

  // Infer sensible defaults by section
  switch (section) {
    case 'timelines':
      return 'timeline';
    case 'frameworks':
      return 'framework';
    case 'sources':
      return 'source';
    case 'constitutions':
    case 'legislative':
      return 'reference';
    case 'pages':
    default:
      return 'page';
  }
}

/**
 * Learning hooks (for immersive / experiential modules later):
 * Keep this purely declarative metadata for now.
 */
function normalizeLearning(meta) {
  const learning = typeof meta.learning === 'object' && meta.learning ? meta.learning : {};

  const mode = typeof learning.mode === 'string' ? learning.mode.trim() : '';
  const estimatedMinutes =
    typeof learning.estimatedMinutes === 'number' && Number.isFinite(learning.estimatedMinutes)
      ? learning.estimatedMinutes
      : undefined;

  const interactives = normalizeStringArray(learning.interactives);

  return {
    mode: mode || '',
    estimatedMinutes: estimatedMinutes ?? null,
    interactives
  };
}

function indexFolder(section, folderRel) {
  const folderAbs = path.join(CONTENT_ROOT, folderRel);
  if (!fs.existsSync(folderAbs)) {
    // Do NOT create folders on demand here. Missing folders should be visible as a project issue.
    return [];
  }

  const files = fg.sync(['**/*.md'], { cwd: folderAbs, dot: false });

  return files.map((rel) => {
    const full = path.join(folderAbs, rel);
    const raw = fs.readFileSync(full, 'utf8');
    const parsed = matter(raw);
    const meta = parsed.data ?? {};

    const relNoExt = rel.replace(/\.md$/i, '');
    const slugPath = toUrlPath(relNoExt);

    // Route convention (current system):
    //  - pages -> /p/<slug>
    //  - timelines -> /timeline/<slug>
    //  - frameworks -> /power/<slug>
    //  - constitutions -> /constitutions/<slug>
    //  - legislative-process -> /legislative/<slug>
    //  - sources -> /sources/<slug>
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

    const title =
      typeof meta.title === 'string' && meta.title.trim().length > 0 ? meta.title.trim() : slugPath;
    const description = typeof meta.description === 'string' ? meta.description.trim() : '';

    const tags = normalizeTags(meta.tags);

    // Formal content → dashboard contract fields
    const l2Topics = normalizeL2Topics(meta.l2Topics ?? meta.l2 ?? meta.level2 ?? meta.topic ?? []);
    const contentType = normalizeContentType(meta, section);
    const learning = normalizeLearning(meta);

    // Optional common metadata
    const date = typeof meta.date === 'string' ? meta.date.trim() : '';
    const era = typeof meta.era === 'string' ? meta.era.trim() : '';
    const place = typeof meta.place === 'string' ? meta.place.trim() : '';

    // Optional provenance fields
    const sourceUrl = typeof meta.sourceUrl === 'string' ? meta.sourceUrl.trim() : '';
    const citation = typeof meta.citation === 'string' ? meta.citation.trim() : '';

    return {
      section,
      slug: slugPath,
      url,
      title,
      description,
      tags,
      l2Topics,
      contentType,
      learning,
      date,
      era,
      place,
      sourceUrl,
      citation,
      // Internal/provenance (debug + tooling)
      sourcePath: toUrlPath(path.relative(CONTENT_ROOT, full))
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

  // Build tag index
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

  // Build Level 2 topic index (contract-ready)
  const l2Map = new Map();
  for (const item of items) {
    for (const t of item.l2Topics ?? []) {
      if (!l2Map.has(t)) l2Map.set(t, []);
      l2Map.get(t).push(item.url);
    }
  }

  const l2Topics = Array.from(l2Map.entries())
    .map(([topic, urls]) => ({
      topic,
      count: urls.length,
      urls: urls.sort()
    }))
    .sort((a, b) => a.topic.localeCompare(b.topic));

  const payload = {
    generatedAt: new Date().toISOString(),
    contentRoot: toUrlPath(CONTENT_ROOT),
    count: items.length,
    items: items.sort((a, b) => a.url.localeCompare(b.url)),
    tags,
    l2Topics
  };

  fs.writeFileSync(OUT_FILE, JSON.stringify(payload, null, 2), 'utf8');
  console.log(`[build-content-index] Wrote: ${OUT_FILE}`);
  console.log(`[build-content-index] Content root: ${CONTENT_ROOT}`);
  console.log(`[build-content-index] Items indexed: ${items.length}`);
  console.log(`[build-content-index] Tags indexed: ${tags.length}`);
  console.log(`[build-content-index] L2 topics indexed: ${l2Topics.length}`);
}

main();
