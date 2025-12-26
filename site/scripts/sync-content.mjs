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

	console.log('[sync-content] Done.');
}

main();
