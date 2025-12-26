---
title: "site_svelte.config.js_"
description: "import adapter from '@sveltejs/adapter-netlify';"
tags:
  - migration:uncategorized
---

site/svelte.config.js

import adapter from '@sveltejs/adapter-netlify';

import { mdsvex } from 'mdsvex';

const config = {

extensions: \['.svelte', '.svx', '.md'\],

preprocess: \[

mdsvex({

extensions: \['.svx', '.md'\]

})

\],

kit: {

adapter: adapter({

// edge: false, // default; enable later only if you intentionally target Netlify Edge

// split: false // default; keep default unless you have a reason

})

}

};

export default config;
