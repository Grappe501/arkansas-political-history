import fs from 'node:fs';
import path from 'node:path';

const ROOT = process.cwd();
const SOURCE = path.join(ROOT, 'content');
const DEST = path.join(ROOT, 'src', 'content'); // ✅ FIX: remove the extra "site"

function ensureDir(p) {
	fs.mkdirSync(p, { recursive: true });
}

function copyDir(src, dest) {
	ensureDir(dest);

	// Node 18+ supports fs.cpSync
	fs.cpSync(src, dest, {
		recursive: true,
		force: true,
		filter: (srcPath) => {
			// Skip OS junk / temp files
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
	}

	console.log(`[sync-content] Syncing content:`);
	console.log(`  from: ${SOURCE}`);
	console.log(`  to:   ${DEST}`);

	// Clear destination first to avoid stale deletes
	if (fs.existsSync(DEST)) {
		fs.rmSync(DEST, { recursive: true, force: true });
	}

	copyDir(SOURCE, DEST);

	console.log('[sync-content] Done.');
}

main();
