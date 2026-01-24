<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { siteConfig } from '$lib/siteConfig';
  
    $: locale = $page.params.locale ?? 'en';
  
    type AudienceMode = 'students' | 'everyday' | 'activists' | 'journalists' | 'policy';
  
    const MODE_LABEL: Record<AudienceMode, string> = {
      students: 'Students',
      everyday: 'Everyday Arkansans',
      activists: 'Activists',
      journalists: 'Journalists',
      policy: 'Policy Makers'
    };
  
    const MODE_COPY: Record<
      AudienceMode,
      {
        headline: string;
        lede: string;
        primaryLabel: string;
        primaryHref: string;
        secondaryLabel: string;
        secondaryHref: string;
        focus: string[];
        intel: string[];
        starterQuestions: string[];
        quickMoves: { label: string; href: string; note: string }[];
      }
    > = {
      students: {
        headline: 'Learn power the way it actually works — not the way textbooks pretend.',
        lede:
          'Trace decisions across time, connect them to institutions, and explain power in plain language—so you can write, debate, and build civic muscle.',
        primaryLabel: 'Start the Timeline',
        primaryHref: '/timeline',
        secondaryLabel: 'See the System Map',
        secondaryHref: '/power',
        focus: ['How rules get made', 'What changed & when', 'Sources you can cite'],
        intel: ['Build citations fast', 'Learn the machinery', 'Turn patterns into arguments'],
        starterQuestions: [
          'What decision changed the rules—and who asked for it?',
          'Which institution enforces this, and what power does it have?',
          'Where is the original document or vote record?'
        ],
        quickMoves: [
          { label: 'Timeline: Turning points', href: '/timeline', note: 'Learn the sequence that built today.' },
          { label: 'Power Map: Institutions', href: '/power', note: 'See who can say yes/no.' },
          { label: 'Sources & Provenance', href: '/l2/sources', note: 'Cite primary documents.' }
        ]
      },
      everyday: {
        headline: 'Start here if you’ve ever felt like the rules weren’t written for you.',
        lede:
          'This is a civic archive built for regular people. We map how power moves—money, institutions, enforcement—so you can recognize patterns and dig deeper with clarity.',
        primaryLabel: 'Enter through the Timeline',
        primaryHref: '/timeline',
        secondaryLabel: 'Show me the Power Map',
        secondaryHref: '/power',
        focus: ['What happened to us', 'Who benefits', 'What you can do next'],
        intel: ['Find “why” fast', 'Follow receipts', 'Turn confusion into clarity'],
        starterQuestions: [
          'Who benefits if this stays confusing?',
          'What rule made this harder for regular people?',
          'What’s the next step I can take today?'
        ],
        quickMoves: [
          { label: 'Timeline: Find the moment', href: '/timeline', note: 'Start with “when did this begin?”' },
          { label: 'Power Map: Who benefits', href: '/power', note: 'See incentives and leverage.' },
          { label: 'Level 2: Learn fast', href: '/l2', note: 'Tracks built to turn knowledge into action.' }
        ]
      },
      activists: {
        headline: 'Turn history into strategy: where to push, who to watch, what leverage works.',
        lede:
          'This isn’t just reading. It’s a training ground—patterns, pressure points, and documented receipts you can use to organize, message, and win fights.',
        primaryLabel: 'Go to Level 2 Tracks',
        primaryHref: '/l2',
        secondaryLabel: 'Find leverage in Power Map',
        secondaryHref: '/power',
        focus: ['Leverage points', 'Message + receipts', 'From knowledge → action'],
        intel: ['Spot choke points', 'Find allies + opponents', 'Build a plan with proof'],
        starterQuestions: [
          'What’s the smallest pressure point that changes the whole system?',
          'Who has the power to block or advance this—and why?',
          'What proof do we need to move people?'
        ],
        quickMoves: [
          { label: 'Level 2 Tracks', href: '/l2', note: 'Structured learning → action.' },
          { label: 'Sources & Provenance', href: '/l2/sources', note: 'Receipts that survive pushback.' },
          { label: 'Power Map: Leverage', href: '/power', note: 'Where pressure actually works.' }
        ]
      },
      journalists: {
        headline: 'A reporting-grade archive: timeline, receipts, and cross-links that save you weeks.',
        lede:
          'Follow the paper trail: primary sources, structured tags, and a map of institutions so you can connect today’s headlines to the machinery underneath.',
        primaryLabel: 'Browse Sources & Provenance',
        primaryHref: '/l2/sources',
        secondaryLabel: 'Start with Timeline',
        secondaryHref: '/timeline',
        focus: ['Receipts first', 'Patterns over scandals', 'Trace claims to documents'],
        intel: ['Cut research time', 'Connect the dots', 'Publish with confidence'],
        starterQuestions: [
          'What’s the earliest document that proves this pattern?',
          'Who changed the rule—and what did they say publicly?',
          'Which orgs funded or lobbied for the shift?'
        ],
        quickMoves: [
          { label: 'Sources & Provenance', href: '/l2/sources', note: 'Primary documents and citations.' },
          { label: 'Timeline: Context', href: '/timeline', note: 'Turn a headline into a story arc.' },
          { label: 'Power Map: Actors', href: '/power', note: 'Institutions, money, enforcement.' }
        ]
      },
      policy: {
        headline: 'See the downstream impact: how policy choices rewire power over decades.',
        lede:
          'Use structured context—institutions, enforcement, and communities affected—to evaluate policy outcomes beyond the talking points.',
        primaryLabel: 'Study the System Map',
        primaryHref: '/power',
        secondaryLabel: 'Review Timeline turning points',
        secondaryHref: '/timeline',
        focus: ['Systems thinking', 'Unintended consequences', 'Institutional incentives'],
        intel: ['See incentives clearly', 'Anticipate consequences', 'Audit outcomes honestly'],
        starterQuestions: [
          'What incentive does this create for the institution?',
          'Who bears the cost if the policy fails?',
          'What guardrails prevent capture?'
        ],
        quickMoves: [
          { label: 'Power Map: System view', href: '/power', note: 'Institutions + enforcement.' },
          { label: 'Timeline: Decisions', href: '/timeline', note: 'What changed—and why.' },
          { label: 'Level 2: Evidence', href: '/l2', note: 'Cases, sources, and outcomes.' }
        ]
      }
    };
  
    const sections = [
      { id: 'heard', label: "Here’s what we heard", key: '1' },
      { id: 'based', label: 'Based on what we heard…', key: '2' },
      { id: 'how', label: 'How we get there', key: '3' },
      { id: 'build', label: 'What’s inside the archive', key: '4' },
      { id: 'use', label: 'How to use this (fast)', key: '5' },
      { id: 'start', label: 'Start with a question', key: '6' },
      { id: 'one', label: 'If you only do one thing…', key: '7' }
    ];
  
    const doors = [
      {
        eyebrow: 'Door 1',
        title: 'Learn the Story',
        desc: 'A guided timeline of turning points—how today’s rules were built, reinforced, and normalized.',
        href: (loc: string) => `/${loc}/timeline`,
        bullets: ['Key eras → key decisions', 'See patterns repeat', 'Understand “how we got here”']
      },
      {
        eyebrow: 'Door 2',
        title: 'Learn the System',
        desc: 'A power map you can use—institutions, money flows, enforcement, and who benefits.',
        href: (loc: string) => `/${loc}/power`,
        bullets: ['Institutions & leverage points', 'Power frameworks (plain language)', 'Cross-links to sources']
      },
      {
        eyebrow: 'Door 3',
        title: 'Dig Deeper (Level 2)',
        desc: 'Structured learning tracks—cases, process, people, money, sources—built to unlock civic action.',
        href: (loc: string) => `/${loc}/l2`,
        bullets: ['Choose a track', 'Build understanding fast', 'Turn knowledge into strategy']
      }
    ];
  
    function hrefFor(path: string) {
      const p = path.startsWith('/') ? path : `/${path}`;
      return `/${locale}${p}`;
    }
  
    // --------- State ---------
    let railOpen = true;
    let intelOpen = true;
    let paletteOpen = false;
  
    let progress = 0; // 0..1
    let activeSection = sections[0]?.id ?? 'heard';
    let mode: AudienceMode = 'everyday';
  
    // Pointer spotlight
    let mx = 0;
    let my = 0;
  
    // Background parallax
    let px = 0;
    let py = 0;
  
    // Command palette search
    let query = '';
  
    function setRail(open: boolean) {
      railOpen = open;
      try {
        localStorage.setItem('aph_rail_open', open ? '1' : '0');
      } catch {}
    }
  
    function setIntel(open: boolean) {
      intelOpen = open;
      try {
        localStorage.setItem('aph_intel_open', open ? '1' : '0');
      } catch {}
    }
  
    function setMode(m: AudienceMode) {
      mode = m;
      try {
        localStorage.setItem('aph_start_mode', m);
      } catch {}
    }
  
    function cycleMode() {
      const order: AudienceMode[] = ['everyday', 'students', 'activists', 'journalists', 'policy'];
      const i = order.indexOf(mode);
      setMode(order[(i + 1) % order.length]);
    }
  
    function jumpTo(id: string) {
      const el = document.getElementById(id);
      if (!el) return;
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  
    function openPalette() {
      paletteOpen = true;
      query = '';
      setTimeout(() => {
        const inp = document.getElementById('cmdk') as HTMLInputElement | null;
        inp?.focus();
      }, 0);
    }
  
    function closePalette() {
      paletteOpen = false;
      query = '';
    }
  
    function chooseAction(href?: string, sectionId?: string, modePick?: AudienceMode) {
      if (modePick) setMode(modePick);
      if (sectionId) jumpTo(sectionId);
      if (href) window.location.href = hrefFor(href);
      closePalette();
    }
  
    const paletteActions = [
      { group: 'Navigate', label: 'Start Here (top)', run: () => window.scrollTo({ top: 0, behavior: 'smooth' }) },
  
      ...sections.map((s) => ({
        group: 'Navigate',
        label: `Jump: ${s.label}`,
        run: () => jumpTo(s.id)
      })),
  
      { group: 'Enter', label: 'Open Timeline', run: () => chooseAction('/timeline') },
      { group: 'Enter', label: 'Open Power Map', run: () => chooseAction('/power') },
      { group: 'Enter', label: 'Open Level 2', run: () => chooseAction('/l2') },
      { group: 'Enter', label: 'Open Sources & Provenance', run: () => chooseAction('/l2/sources') },
  
      { group: 'Audience', label: 'Mode: Everyday Arkansans', run: () => chooseAction(undefined, undefined, 'everyday') },
      { group: 'Audience', label: 'Mode: Students', run: () => chooseAction(undefined, undefined, 'students') },
      { group: 'Audience', label: 'Mode: Activists', run: () => chooseAction(undefined, undefined, 'activists') },
      { group: 'Audience', label: 'Mode: Journalists', run: () => chooseAction(undefined, undefined, 'journalists') },
      { group: 'Audience', label: 'Mode: Policy Makers', run: () => chooseAction(undefined, undefined, 'policy') },
  
      { group: 'Tools', label: 'Toggle Investigation Rail', run: () => setRail(!railOpen) },
      { group: 'Tools', label: 'Toggle Intel Strip', run: () => setIntel(!intelOpen) }
    ];
  
    $: filteredActions = paletteActions.filter((a) =>
      (a.label + ' ' + a.group).toLowerCase().includes(query.trim().toLowerCase())
    );
  
    onMount(() => {
      document.body.classList.add('start-here');
  
      try {
        const v = localStorage.getItem('aph_rail_open');
        if (v === '0') railOpen = false;
      } catch {}
  
      try {
        const v = localStorage.getItem('aph_intel_open');
        if (v === '0') intelOpen = false;
      } catch {}
  
      try {
        const m = (localStorage.getItem('aph_start_mode') ?? 'everyday') as AudienceMode;
        if (MODE_COPY[m]) mode = m;
      } catch {}
  
      // seed cursor spotlight
      mx = Math.round(window.innerWidth * 0.55);
      my = Math.round(window.innerHeight * 0.22);
  
      const onScroll = () => {
        const doc = document.documentElement;
        const scrollTop = doc.scrollTop || document.body.scrollTop || 0;
        const height = doc.scrollHeight - doc.clientHeight;
        progress = height > 0 ? Math.max(0, Math.min(1, scrollTop / height)) : 0;
      };
  
      const targets = sections.map((s) => document.getElementById(s.id)).filter(Boolean) as HTMLElement[];
  
      const io = new IntersectionObserver(
        (entries) => {
          const visible = entries
            .filter((e) => e.isIntersecting)
            .sort((a, b) => (b.intersectionRatio ?? 0) - (a.intersectionRatio ?? 0))[0];
          if (visible?.target?.id) activeSection = visible.target.id;
        },
        { root: null, rootMargin: '-20% 0px -65% 0px', threshold: [0.05, 0.1, 0.2, 0.35, 0.5] }
      );
  
      targets.forEach((t) => io.observe(t));
  
      const onPointer = (e: PointerEvent) => {
        mx = e.clientX;
        my = e.clientY;
        const cx = window.innerWidth / 2;
        const cy = window.innerHeight / 2;
        px = Math.max(-1, Math.min(1, (e.clientX - cx) / cx));
        py = Math.max(-1, Math.min(1, (e.clientY - cy) / cy));
      };
  
      const onKey = (e: KeyboardEvent) => {
        if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
          const t = e.target as HTMLElement | null;
          const tag = t?.tagName?.toLowerCase();
          if (tag !== 'input' && tag !== 'textarea') {
            e.preventDefault();
            openPalette();
          }
        }
  
        if (e.key === 'Escape' && paletteOpen) {
          e.preventDefault();
          closePalette();
        }
  
        if (!paletteOpen) {
          const s = sections.find((x) => x.key === e.key);
          if (s) {
            e.preventDefault();
            jumpTo(s.id);
          }
          if (e.key === 'r' || e.key === 'R') {
            e.preventDefault();
            setRail(!railOpen);
          }
          if (e.key === 'm' || e.key === 'M') {
            e.preventDefault();
            cycleMode();
          }
        }
      };
  
      onScroll();
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('pointermove', onPointer, { passive: true });
      window.addEventListener('keydown', onKey);
  
      return () => {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('pointermove', onPointer);
        window.removeEventListener('keydown', onKey);
        io.disconnect();
        document.body.classList.remove('start-here');
      };
    });
  </script>
  
  <svelte:head>
    <title>Start Here • {siteConfig.siteName}</title>
    <meta
      name="description"
      content="A hopeful, urgent, investigative entry point into Arkansas political history—built to help everyday people understand power and dig deeper."
    />
  </svelte:head>
  
  <div class="startHereShell">
    <!-- top progress bar -->
    <div class="progress" aria-hidden="true">
      <div class="progress-bar" style={`transform: scaleX(${progress});`}></div>
    </div>
  
    <!-- cursor spotlight -->
    <div class="spotlight" aria-hidden="true" style={`transform: translate3d(${mx}px, ${my}px, 0);`}></div>
  
    <!-- aurora/parallax -->
    <div class="aurora" aria-hidden="true" style={`--px:${px}; --py:${py};`}></div>
  
    <section class="stage" aria-label="Start Here stage">
      <!-- LEFT: Investigation Rail -->
      <aside class={`rail ${railOpen ? 'open' : 'closed'}`} aria-label="Investigation rail">
        <div class="rail-inner">
          <div class="rail-header">
            <div class="rail-title">Investigation Rail</div>
            <button class="rail-toggle" type="button" on:click={() => setRail(!railOpen)}>
              {railOpen ? 'Hide' : 'Show'}
            </button>
          </div>
  
          <div class="rail-pill-row" aria-label="Tone">
            <span class="pill hopeful">Hopeful</span>
            <span class="pill urgent">Urgent</span>
            <span class="pill investigative">Investigative</span>
          </div>
  
          <div class="rail-block">
            <div class="kicker">Audience</div>
            <div class="mode" role="tablist" aria-label="Audience mode">
              {#each (Object.keys(MODE_LABEL) as AudienceMode[]) as m (m)}
                <button
                  type="button"
                  class={`mode-btn ${mode === m ? 'active' : ''}`}
                  role="tab"
                  aria-selected={mode === m}
                  on:click={() => setMode(m)}
                >
                  {MODE_LABEL[m]}
                </button>
              {/each}
            </div>
            <div class="tinyhint"><span class="kbd">M</span> cycle mode</div>
          </div>
  
          <div class="rail-block">
            <div class="kicker">Sections</div>
            <nav class="rail-nav" aria-label="Jump to section">
              {#each sections as s (s.id)}
                <button
                  class={`rail-link ${activeSection === s.id ? 'active' : ''}`}
                  type="button"
                  on:click={() => jumpTo(s.id)}
                >
                  <span class="dot" aria-hidden="true"></span>
                  <span class="lbl">{s.label}</span>
                  <span class="kbd">{s.key}</span>
                </button>
              {/each}
            </nav>
          </div>
  
          <div class="rail-block">
            <div class="kicker">Next best move</div>
            <a class="rail-cta primary" href={hrefFor(MODE_COPY[mode].primaryHref)}>
              {MODE_COPY[mode].primaryLabel}
            </a>
            <a class="rail-cta" href={hrefFor(MODE_COPY[mode].secondaryHref)}>
              {MODE_COPY[mode].secondaryLabel}
            </a>
          </div>
  
          <div class="rail-block">
            <div class="kicker">Command</div>
            <button class="rail-cta cmdk" type="button" on:click={openPalette}>
              Open Command Palette <span class="kbd">/</span>
            </button>
            <div class="tinyhint"><span class="kbd">R</span> toggle rail</div>
          </div>
        </div>
      </aside>
  
      <!-- CENTER: Content -->
      <div class="content">
        <header class="hero" aria-label="Start Here hero">
          <div class="hero-grid">
            <div class="hero-left">
              <div class="badge">
                <span class="badge-dot" aria-hidden="true"></span>
                <span>Stand Up Arkansas • Civic Archive</span>
                <span class="badge-tag">Start Here</span>
              </div>
  
              <h1 class="headline">{MODE_COPY[mode].headline}</h1>
  
              <p class="lede">{MODE_COPY[mode].lede}</p>
  
              <div class="hero-actions" aria-label="Primary actions">
                <a class="cta primary" href={hrefFor(MODE_COPY[mode].primaryHref)}>{MODE_COPY[mode].primaryLabel}</a>
                <a class="cta ghost" href={hrefFor(MODE_COPY[mode].secondaryHref)}>{MODE_COPY[mode].secondaryLabel}</a>
                <button class="cta ghost" type="button" on:click={openPalette}>Command <span class="kbd">/</span></button>
              </div>
  
              <div class="hero-strip" aria-label="Guiding principle">
                <div class="strip-k">STRUCTURE BEATS OVERWHELM</div>
                <div class="strip-v">Move from “I’m lost” → “I see it” → “I can explain it.”</div>
              </div>
            </div>
  
            <div class="hero-right" aria-label="Briefing panel">
              <div class="brief">
                <div class="brief-top">
                  <div class="kicker">Briefing</div>
                  <div class="brief-title">{MODE_LABEL[mode]} focus</div>
                </div>
  
                <ul class="brief-list" aria-label="What this page gives you">
                  {#each MODE_COPY[mode].focus as f (f)}
                    <li>{f}</li>
                  {/each}
                </ul>
  
                <div class="brief-note">
                  <span class="note-strong">Rule:</span> don’t read everything. Choose one door and follow it until you can explain it.
                </div>
  
                <div class="brief-mini">
                  <div class="mini">
                    <div class="mini-k">Promise</div>
                    <div class="mini-v">Receipts + structure. No fog.</div>
                  </div>
                  <div class="mini">
                    <div class="mini-k">Method</div>
                    <div class="mini-v">Timeline → system → sources</div>
                  </div>
                </div>
  
                <div class="brief-intel">
                  <div class="mini-k">Intel</div>
                  <ul>
                    {#each MODE_COPY[mode].intel as i (i)}
                      <li>{i}</li>
                    {/each}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </header>
  
        <!-- main content continues in Chunk 2 -->
        <main class="main">
            <!-- 1) Here’s what we heard -->
            <section class="panel" id="heard">
              <div class="panel-top">
                <h2 class="panel-title">Here’s what we heard</h2>
                <p class="panel-sub">
                  People don’t avoid civic life because they don’t care. They avoid it because the system is built to be hard to see.
                </p>
              </div>
    
              <div class="grid-3" role="list" aria-label="What people experience">
                <div class="card" role="listitem">
                  <div class="card-title">Confusion that feels personal</div>
                  <p class="card-body">You’re told you “should’ve known,” but nobody taught you how the machinery works—on purpose.</p>
                </div>
    
                <div class="card" role="listitem">
                  <div class="card-title">Decisions made elsewhere</div>
                  <p class="card-body">Outcomes feel predetermined because power is organized—through institutions, money, and rules.</p>
                </div>
    
                <div class="card" role="listitem">
                  <div class="card-title">Information without a map</div>
                  <p class="card-body">You can read a thousand articles and still miss the pattern. This gives you the map.</p>
                </div>
              </div>
            </section>
    
            <!-- 2) Based on what we heard… -->
            <section class="panel emphasis" id="based">
              <div class="panel-top">
                <h2 class="panel-title">Based on what we heard and the policies and positions we will promote</h2>
                <p class="panel-sub">
                  We’re building a learning system that turns history into usable knowledge—so regular people can recognize power patterns,
                  verify claims, and act with confidence.
                </p>
              </div>
    
              <div class="principles" aria-label="Core principles">
                <div class="principle">
                  <div class="p-k">Moral clarity</div>
                  <div class="p-v">We name who benefits and who pays—without burying the truth in polite language.</div>
                </div>
                <div class="principle">
                  <div class="p-k">Sources matter</div>
                  <div class="p-v">Claims should trace back to documents, records, or a credible citation trail.</div>
                </div>
                <div class="principle">
                  <div class="p-k">Structure beats overwhelm</div>
                  <div class="p-v">Move from “I’m lost” → “I see it” → “I can explain it.”</div>
                </div>
              </div>
            </section>
    
            <!-- 3) How we get there -->
            <section class="panel" id="how">
              <div class="panel-top">
                <h2 class="panel-title">How we get there</h2>
                <p class="panel-sub">Choose one door. Don’t try to read everything. This is designed to reward focus.</p>
              </div>
    
              <div class="doors" aria-label="Choose your entry path">
                {#each doors as d (d.title)}
                  <a class="door" href={d.href(locale)}>
                    <div class="door-top">
                      <div class="door-eyebrow">{d.eyebrow}</div>
                      <div class="door-title">{d.title}</div>
                      <div class="door-desc">{d.desc}</div>
                    </div>
    
                    <ul class="door-bullets" aria-label="What you'll get">
                      {#each d.bullets as b (b)}
                        <li>{b}</li>
                      {/each}
                    </ul>
    
                    <div class="door-cta">
                      <span class="door-cta-text">Open this door</span>
                      <span class="door-cta-arrow" aria-hidden="true">→</span>
                    </div>
                  </a>
                {/each}
              </div>
            </section>
    
            <!-- 4) What’s inside the archive -->
            <section class="panel" id="build">
              <div class="panel-top">
                <h2 class="panel-title">What’s inside the archive</h2>
                <p class="panel-sub">
                  Not a blog feed. A structured system: timeline → institutions → sources → patterns → action.
                </p>
              </div>
    
              <div class="grid-3">
                <div class="card">
                  <div class="card-title">Timeline moments</div>
                  <p class="card-body">
                    Turning points that explain why today looks like today—built for “follow the trail” learning.
                  </p>
                  <div class="card-links">
                    <a class="chip" href={hrefFor('/timeline')}>Open Timeline</a>
                  </div>
                </div>
    
                <div class="card">
                  <div class="card-title">Power Map</div>
                  <p class="card-body">
                    Institutions, money flows, enforcement, and leverage—so you can stop guessing where pressure works.
                  </p>
                  <div class="card-links">
                    <a class="chip" href={hrefFor('/power')}>Open Power Map</a>
                  </div>
                </div>
    
                <div class="card">
                  <div class="card-title">Sources & Provenance</div>
                  <p class="card-body">
                    Receipts-first research: documents, citations, and a trail you can defend when it gets contested.
                  </p>
                  <div class="card-links">
                    <a class="chip" href={hrefFor('/l2/sources')}>Browse Sources</a>
                  </div>
                </div>
              </div>
            </section>
    
            <!-- 5) How to use this (fast) -->
            <section class="panel emphasis" id="use">
              <div class="panel-top">
                <h2 class="panel-title">How to use this (fast)</h2>
                <p class="panel-sub">
                  Pick one thread. Follow it until you can explain it. Then you’re ready for Level 3 action.
                </p>
              </div>
    
              <div class="steps" aria-label="Fast method steps">
                <div class="step">
                  <div class="step-k">Step 1</div>
                  <div class="step-v">Start with a moment on the timeline.</div>
                  <div class="step-s">Answer: what changed?</div>
                </div>
                <div class="step">
                  <div class="step-k">Step 2</div>
                  <div class="step-v">Open the system map.</div>
                  <div class="step-s">Answer: who can say yes/no?</div>
                </div>
                <div class="step">
                  <div class="step-k">Step 3</div>
                  <div class="step-v">Pull the original source.</div>
                  <div class="step-s">Answer: what does the record actually show?</div>
                </div>
                <div class="step">
                  <div class="step-k">Step 4</div>
                  <div class="step-v">Name the pattern.</div>
                  <div class="step-s">Answer: who benefits—and who pays?</div>
                </div>
              </div>
    
              <div class="quickMoves" aria-label="Quick moves">
                <div class="qm-title">Quick moves for {MODE_LABEL[mode]}</div>
                <div class="qm-grid">
                  {#each MODE_COPY[mode].quickMoves as q (q.label)}
                    <a class="qm" href={hrefFor(q.href)}>
                      <div class="qm-l">{q.label}</div>
                      <div class="qm-n">{q.note}</div>
                    </a>
                  {/each}
                </div>
              </div>
            </section>
    
            <!-- 6) Start with a question -->
            <section class="panel" id="start">
              <div class="panel-top">
                <h2 class="panel-title">Start with a question</h2>
                <p class="panel-sub">
                  This site works best when you bring one clear question and chase it all the way to the record.
                </p>
              </div>
    
              <div class="grid-3">
                {#each MODE_COPY[mode].starterQuestions as q (q)}
                  <div class="card">
                    <div class="card-title">Question</div>
                    <p class="card-body">{q}</p>
                    <div class="card-links">
                      <button class="chip" type="button" on:click={openPalette}>Use Command <span class="kbd">/</span></button>
                    </div>
                  </div>
                {/each}
              </div>
            </section>
    
            <!-- 7) If you only do one thing… -->
            <section class="panel closing" id="one">
              <div class="closing-inner">
                <h2 class="closing-title">If you only do one thing today…</h2>
                <p class="closing-body">
                  Pick one topic or one timeline moment and follow the links until you can explain it in your own words.
                  That’s how power loses its fog.
                </p>
    
                <div class="closing-actions">
                  <a class="cta primary" href={hrefFor('/timeline')}>Start with the Timeline</a>
                  <a class="cta ghost" href={hrefFor('/l2')}>Go to Level 2</a>
                  <button class="cta ghost" type="button" on:click={openPalette}>Pick a trail <span class="kbd">/</span></button>
                </div>
    
                <p class="fineprint">
                  Designed like a briefing: choose a mode, choose a door, and follow the trail. This is how we build power literacy.
                </p>
              </div>
            </section>
          </main>
        </div>
    
        <!-- RIGHT: Intel Strip -->
        <aside class={`intel ${intelOpen ? 'open' : 'closed'}`} aria-label="Intel strip">
          <div class="intel-inner">
            <div class="intel-head">
              <div class="intel-title">Intel</div>
              <button class="intel-toggle" type="button" on:click={() => setIntel(!intelOpen)}>
                {intelOpen ? 'Hide' : 'Show'}
              </button>
            </div>
    
            <div class="intel-block">
              <div class="kicker">Mode</div>
              <div class="intel-pill">{MODE_LABEL[mode]}</div>
              <div class="tinyhint">Press <span class="kbd">M</span> to cycle.</div>
            </div>
    
            <div class="intel-block">
              <div class="kicker">Section</div>
              <div class="intel-pill">{sections.find((s) => s.id === activeSection)?.label ?? '—'}</div>
              <div class="tinyhint">Press <span class="kbd">1</span>–<span class="kbd">7</span> to jump.</div>
            </div>
    
            <div class="intel-block">
              <div class="kicker">Next move</div>
              <a class="intel-cta primary" href={hrefFor(MODE_COPY[mode].primaryHref)}>{MODE_COPY[mode].primaryLabel}</a>
              <a class="intel-cta" href={hrefFor(MODE_COPY[mode].secondaryHref)}>{MODE_COPY[mode].secondaryLabel}</a>
            </div>
    
            <div class="intel-block">
              <div class="kicker">Shortcuts</div>
              <div class="shortcuts">
                <div class="sc"><span class="kbd">/</span><span>Command palette</span></div>
                <div class="sc"><span class="kbd">R</span><span>Toggle rail</span></div>
                <div class="sc"><span class="kbd">M</span><span>Cycle mode</span></div>
                <div class="sc"><span class="kbd">1–7</span><span>Jump sections</span></div>
              </div>
            </div>
    
            <div class="intel-block">
              <div class="kicker">This is built to feel different</div>
              <div class="intel-copy">Not “a page.” A briefing interface. A trail selector. A research cockpit.</div>
            </div>
          </div>
        </aside>
      </section>
    
      <!-- Command Palette -->
      {#if paletteOpen}
        <div class="paletteOverlay" role="presentation" on:click|self={closePalette}>
          <div class="palette" role="dialog" aria-modal="true" aria-label="Command palette">
            <div class="paletteTop">
              <div class="paletteTitle">Command</div>
              <button class="paletteClose" type="button" on:click={closePalette}>Esc</button>
            </div>
    
            <input
              id="cmdk"
              class="paletteInput"
              type="text"
              bind:value={query}
              placeholder="Type to search actions… (Timeline, Power, Sources, Mode, Jump)"
              aria-label="Search commands"
            />
    
            <div class="paletteList" role="list">
              {#if filteredActions.length === 0}
                <div class="paletteEmpty">No matches.</div>
              {:else}
                {#each filteredActions as a (a.group + a.label)}
                  <button class="paletteItem" type="button" on:click={a.run} role="listitem">
                    <span class="paletteGroup">{a.group}</span>
                    <span class="paletteLabel">{a.label}</span>
                  </button>
                {/each}
              {/if}
            </div>
    
            <div class="paletteFooter">
              <span>Tip: press <span class="kbd">/</span> anywhere</span>
              <span class="sep">•</span>
              <span>Esc closes</span>
            </div>
          </div>
        </div>
      {/if}
    </div>
    
    <!-- styles in Chunk 3 -->
    <style>
        /* ============================================================
           START HERE — “REVOLUTION UI LAYER”
           Fixes:
             - No gray fog: readable text everywhere
             - 3rd accent color: amber (urgent contrast)
             - Better chips + steps + quick-moves blocks
             - Keeps header glassy on this route
           ============================================================ */
      
        /* Route-only overrides */
        :global(body.start-here) { background: #05070a !important; }
        :global(body.start-here main),
        :global(body.start-here .prose),
        :global(body.start-here .container),
        :global(body.start-here .page),
        :global(body.start-here .wrap),
        :global(body.start-here .content),
        :global(body.start-here .inner),
        :global(body.start-here .layout) {
          max-width: none !important;
          width: 100% !important;
        }
        :global(body.start-here .prose) { opacity: 1 !important; color: inherit !important; }
      
        /* Header glass on this page */
        :global(body.start-here header),
        :global(body.start-here .site-header),
        :global(body.start-here .topbar),
        :global(body.start-here .header) {
          background: rgba(5, 7, 10, 0.35) !important;
          backdrop-filter: blur(12px) saturate(120%);
          border-bottom: 1px solid rgba(255, 255, 255, 0.10) !important;
        }
        :global(body.start-here header a),
        :global(body.start-here .site-header a),
        :global(body.start-here nav a) { color: rgba(241,245,249,0.94) !important; }
        :global(body.start-here header a:hover),
        :global(body.start-here nav a:hover) { color: rgba(255,255,255,1) !important; }
      
        /* Light theme */
        :global(:root[data-resolved-theme='light'] body.start-here) { background: #f7fafc !important; }
        :global(:root[data-resolved-theme='light'] body.start-here header),
        :global(:root[data-resolved-theme='light'] body.start-here .site-header) {
          background: rgba(255, 255, 255, 0.70) !important;
          border-bottom: 1px solid rgba(15, 23, 42, 0.10) !important;
        }
        :global(:root[data-resolved-theme='light'] body.start-here header a),
        :global(:root[data-resolved-theme='light'] body.start-here nav a) { color: rgba(15,23,42,0.88) !important; }
      
        /* Tokens */
        .startHereShell{
          --a:#60a5fa; --b:#a78bfa; --c:#f59e0b; --g:#34d399;
          --bg:#05070a;
          --surface: rgba(11,18,32,0.90);
          --surface2: rgba(15,26,47,0.86);
          --panel: rgba(11,18,32,0.88);
      
          /* CONTRAST FIX: keep “muted” still very readable */
          --ink:#f1f5f9;
          --muted:#e7eef8;    /* brighter than before */
          --subtle:#b6c7de;   /* labels still readable */
      
          --border: rgba(255,255,255,0.14);
          --border2: rgba(255,255,255,0.22);
          --shadow: rgba(0,0,0,0.70);
          --shadow2: rgba(0,0,0,0.45);
      
          position:relative;
          isolation:isolate;
        }
        :global(:root[data-resolved-theme='light']) .startHereShell{
          --bg:#f7fafc;
          --surface:#fff;
          --surface2:#f3f6fb;
          --panel:#fff;
          --ink:#0b1220;
          --muted:#111827;
          --subtle:#475569;
          --border: rgba(15,23,42,0.14);
          --border2: rgba(15,23,42,0.20);
          --shadow: rgba(15,23,42,0.12);
          --shadow2: rgba(15,23,42,0.08);
        }
      
        /* Progress */
        .progress{ position:sticky; top:0; z-index:80; height:3px; background:rgba(255,255,255,.10); }
        :global(:root[data-resolved-theme='light']) .progress{ background:rgba(15,23,42,.10); }
        .progress-bar{ height:100%; transform-origin:left center; background: linear-gradient(90deg,var(--a),var(--b),var(--c)); }
      
        /* Spotlight */
        .spotlight{
          position:fixed; left:-260px; top:-260px; width:520px; height:520px;
          z-index:0; border-radius:999px; pointer-events:none;
          background: radial-gradient(closest-side, rgba(245,158,11,.22), rgba(167,139,250,.16), rgba(96,165,250,.10), transparent 72%);
          filter: blur(2px);
          mix-blend-mode: screen;
          opacity: .95;
        }
        :global(:root[data-resolved-theme='light']) .spotlight{
          mix-blend-mode:multiply; opacity:.32; filter:blur(6px);
        }
      
        /* Aurora */
        .aurora{
          position:fixed; inset:0; z-index:-1; pointer-events:none;
          background:
            radial-gradient(900px 600px at 18% 10%, rgba(96,165,250,.18), transparent 60%),
            radial-gradient(900px 650px at 82% 14%, rgba(167,139,250,.17), transparent 60%),
            radial-gradient(900px 700px at 55% 115%, rgba(245,158,11,.14), transparent 70%),
            radial-gradient(800px 600px at 40% 85%, rgba(52,211,153,.10), transparent 70%),
            var(--bg);
          transform: translate3d(calc(var(--px) * 10px), calc(var(--py) * 10px), 0);
        }
      
        /* Layout */
        .stage{
          min-height:100vh; width:100%;
          display:grid;
          grid-template-columns: 360px minmax(0,1fr) 320px;
          position:relative; z-index:1;
          color:var(--ink);
        }
        .rail,.intel{
          position:sticky; top:3px; height:calc(100vh - 3px);
          padding:1rem;
          backdrop-filter: blur(14px) saturate(130%);
        }
        .rail{ border-right:1px solid var(--border); background:rgba(5,7,10,.55); }
        .intel{ border-left:1px solid var(--border); background:rgba(5,7,10,.45); }
        :global(:root[data-resolved-theme='light']) .rail,
        :global(:root[data-resolved-theme='light']) .intel{ background:rgba(255,255,255,.62); }
      
        .rail.closed{ width:76px; padding:1rem .75rem; }
        .rail.closed .rail-inner > *:not(.rail-header){ display:none; }
        .rail.closed .rail-title{ display:none; }
      
        .intel.closed{ width:70px; padding:1rem .75rem; }
        .intel.closed .intel-inner > *:not(.intel-head){ display:none; }
      
        /* Sheen border */
        .rail-inner,.intel-inner,.hero,.panel,.brief,.door{
          position:relative;
        }
        .rail-inner::before,.intel-inner::before,.hero::before,.panel::before,.brief::before,.door::before{
          content:'';
          position:absolute; inset:-1px;
          border-radius:inherit; padding:1px;
          background: linear-gradient(120deg, rgba(96,165,250,.45), rgba(167,139,250,.35), rgba(245,158,11,.30), rgba(52,211,153,.18));
          -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
          -webkit-mask-composite: xor;
          mask-composite: exclude;
          opacity:.30;
          pointer-events:none;
        }
      
        .rail-inner,.intel-inner{
          border:1px solid var(--border);
          border-radius:18px;
          padding:1rem;
          background: rgba(11,18,32,.88);
          box-shadow: 0 18px 60px var(--shadow);
        }
        :global(:root[data-resolved-theme='light']) .rail-inner,
        :global(:root[data-resolved-theme='light']) .intel-inner{ background: var(--surface); }
      
        .kicker{
          font-size:.78rem;
          letter-spacing:.12em;
          text-transform:uppercase;
          font-weight:950;
          color:var(--subtle);
          margin-bottom:.5rem;
        }
        .kbd{
          display:inline-flex; align-items:center; justify-content:center;
          min-width:1.6rem; height:1.4rem; padding:0 .4rem;
          border-radius:10px;
          border:1px solid var(--border2);
          background: rgba(255,255,255,.06);
          color: var(--ink);
          font-size:.82rem;
          font-weight:900;
          line-height:1;
        }
        :global(:root[data-resolved-theme='light']) .kbd{ background: rgba(15,23,42,.05); }
        .tinyhint{ margin-top:.45rem; color:var(--subtle); font-weight:800; }
      
        /* Rail */
        .rail-header{ display:flex; align-items:center; justify-content:space-between; gap:.75rem; margin-bottom:.75rem; }
        .rail-title{ font-weight:980; letter-spacing:-.02em; }
        .rail-toggle{
          border:1px solid var(--border);
          background:transparent;
          color:var(--ink);
          border-radius:999px;
          padding:.35rem .65rem;
          font-weight:900;
          cursor:pointer;
        }
        .rail-toggle:hover{ background: rgba(255,255,255,.06); }
      
        .rail-pill-row{ display:flex; flex-wrap:wrap; gap:.35rem; margin-bottom:.85rem; }
        .pill{
          border:1px solid var(--border);
          border-radius:999px;
          padding:.18rem .55rem;
          font-weight:950;
          font-size:.82rem;
          color: var(--muted);
          background: rgba(255,255,255,.04);
        }
        .pill.hopeful{ box-shadow: inset 0 0 0 999px rgba(52,211,153,.07); }
        .pill.urgent{ box-shadow: inset 0 0 0 999px rgba(245,158,11,.10); }
        .pill.investigative{ box-shadow: inset 0 0 0 999px rgba(96,165,250,.07); }
      
        .mode{ display:grid; gap:.45rem; }
        .mode-btn{
          text-align:left;
          border:1px solid var(--border);
          border-radius:14px;
          padding:.6rem .7rem;
          background: rgba(255,255,255,.03);
          color: var(--muted);
          font-weight:950;
          cursor:pointer;
          transition: transform 120ms ease, background 120ms ease, border-color 120ms ease;
        }
        .mode-btn:hover{
          background: rgba(255,255,255,.06);
          color: var(--ink);
          transform: translateY(-1px);
          border-color: rgba(255,255,255,.22);
        }
        .mode-btn.active{
          background: linear-gradient(90deg, rgba(96,165,250,.22), rgba(167,139,250,.14), rgba(245,158,11,.12));
          color: var(--ink);
          border-color: rgba(255,255,255,.22);
        }
      
        .rail-nav{ display:grid; gap:.45rem; }
        .rail-link{
          display:grid;
          grid-template-columns: 14px 1fr auto;
          gap:.55rem;
          align-items:center;
          border:1px solid var(--border);
          background: rgba(255,255,255,.03);
          color: var(--muted);
          border-radius:14px;
          padding:.6rem .65rem;
          cursor:pointer;
          text-align:left;
          font-weight:950;
          transition: transform 120ms ease, background 120ms ease, border-color 120ms ease;
        }
        .rail-link:hover{
          background: rgba(255,255,255,.06);
          color: var(--ink);
          transform: translateY(-1px);
          border-color: rgba(255,255,255,.22);
        }
        .rail-link.active{
          color: var(--ink);
          background: linear-gradient(90deg, rgba(96,165,250,.20), rgba(167,139,250,.14), rgba(245,158,11,.12));
          border-color: rgba(255,255,255,.22);
        }
        .dot{ width:10px; height:10px; border-radius:999px; background: rgba(255,255,255,.22); }
        .rail-link.active .dot{ background: linear-gradient(90deg,var(--a),var(--b),var(--c)); }
        .lbl{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
      
        .rail-cta, .intel-cta{
          display:block;
          text-decoration:none;
          border:1px solid var(--border);
          border-radius:14px;
          padding:.75rem .8rem;
          font-weight:980;
          color: var(--ink);
          background: rgba(255,255,255,.03);
          margin-top:.55rem;
          min-height:44px;
          transition: transform 120ms ease, background 120ms ease, border-color 120ms ease;
        }
        .rail-cta:hover, .intel-cta:hover{
          background: rgba(255,255,255,.06);
          transform: translateY(-1px);
          border-color: rgba(255,255,255,.22);
        }
        .rail-cta.primary{
          background: linear-gradient(90deg, rgba(245,158,11,.22), rgba(96,165,250,.16), rgba(167,139,250,.12));
        }
        .intel-cta.primary{
          background: linear-gradient(90deg, rgba(96,165,250,.18), rgba(167,139,250,.14), rgba(245,158,11,.14));
        }
        .rail-cta.cmdk{ text-align:left; }
      
        /* Intel */
        .intel-head{ display:flex; align-items:center; justify-content:space-between; gap:.75rem; margin-bottom:.75rem; }
        .intel-title{ font-weight:980; letter-spacing:-.02em; }
        .intel-toggle{
          border:1px solid var(--border);
          background:transparent;
          color:var(--ink);
          border-radius:999px;
          padding:.35rem .65rem;
          font-weight:900;
          cursor:pointer;
        }
        .intel-toggle:hover{ background: rgba(255,255,255,.06); }
        .intel-block{ margin-top:.9rem; }
        .intel-pill{
          margin-top:.2rem;
          border:1px solid var(--border);
          border-radius:14px;
          padding:.65rem .75rem;
          background: rgba(255,255,255,.03);
          font-weight:950;
          color: var(--ink);
        }
        .shortcuts{ display:grid; gap:.45rem; }
        .sc{
          display:grid;
          grid-template-columns: 56px 1fr;
          align-items:center;
          gap:.6rem;
          color: var(--muted);
          font-weight:900;
        }
        .intel-copy{ color: var(--muted); line-height:1.6; font-weight:850; }
      
        /* Center */
        .content{ min-width:0; padding: clamp(1rem, 3vw, 2.5rem); }
      
        .hero{
          border:1px solid var(--border);
          border-radius:22px;
          background: var(--surface);
          box-shadow: 0 22px 70px var(--shadow);
          padding: clamp(1.1rem, 2.5vw, 1.75rem);
          overflow:hidden;
        }
        .hero::after{
          content:'';
          position:absolute;
          inset:0;
          pointer-events:none;
          opacity:.08;
          background-image: radial-gradient(rgba(255,255,255,.22) 1px, transparent 1px);
          background-size: 22px 22px;
          mix-blend-mode: overlay;
        }
      
        .hero-grid{ display:grid; grid-template-columns: 1.35fr .80fr; gap: clamp(1rem,2.5vw,1.6rem); align-items:start; }
      
        .badge{
          display:inline-flex; align-items:center; gap:.6rem;
          padding:.42rem .75rem;
          border:1px solid var(--border);
          border-radius:999px;
          background: rgba(255,255,255,.04);
          color: var(--muted);
          font-weight:900;
        }
        .badge-tag{
          margin-left:.25rem;
          padding:.18rem .55rem;
          border-radius:999px;
          border:1px solid var(--border2);
          background: rgba(245,158,11,.14);
          color: var(--ink);
          font-weight:950;
        }
        .badge-dot{
          width:10px; height:10px; border-radius:999px;
          background: linear-gradient(90deg,var(--a),var(--b),var(--c));
          box-shadow: 0 0 0 7px rgba(245,158,11,.12), 0 0 0 12px rgba(96,165,250,.08);
        }
      
        .headline{
          margin: 1rem 0 .75rem;
          font-size: clamp(2.15rem, 3.15vw, 3.25rem);
          line-height: 1.02;
          letter-spacing: -.04em;
          font-weight: 995;
          color: var(--ink);
          text-shadow: 0 10px 40px rgba(0,0,0,.35);
        }
        .lede{
          margin:0;
          font-size:1.15rem;
          line-height:1.7;
          color: var(--muted);
          font-weight: 850; /* boost readability */
          max-width: 90ch;
        }
      
        .hero-actions{ display:flex; flex-wrap:wrap; gap:.75rem; margin-top:1.1rem; }
        .cta{
          display:inline-flex; align-items:center; justify-content:center;
          border-radius:16px;
          border:1px solid var(--border);
          padding:.82rem 1.05rem;
          text-decoration:none;
          font-weight:980;
          letter-spacing:-.01em;
          color: var(--ink);
          transition: transform 120ms ease, background 120ms ease, border-color 120ms ease, box-shadow 120ms ease;
          min-height:44px;
          background: rgba(255,255,255,.03);
          cursor:pointer;
        }
        .cta.primary{
          background: linear-gradient(90deg, rgba(245,158,11,.24), rgba(96,165,250,.16), rgba(167,139,250,.14));
          box-shadow: 0 12px 35px rgba(0,0,0,.25);
        }
        .cta:hover{
          transform: translateY(-1px);
          border-color: rgba(255,255,255,.22);
          background: rgba(255,255,255,.06);
          box-shadow: 0 12px 40px rgba(0,0,0,.25);
        }
        .cta:focus-visible{ outline:3px solid rgba(245,158,11,.55); outline-offset:3px; }
      
        .hero-strip{
          margin-top:1rem;
          border:1px dashed rgba(255,255,255,.22);
          border-radius:16px;
          padding:.85rem .9rem;
          background: rgba(255,255,255,.03);
        }
        .strip-k{ font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; font-weight:950; color: var(--subtle); }
        .strip-v{ margin-top:.25rem; font-weight:950; color: var(--ink); }
      
        .brief{
          border:1px solid var(--border);
          border-radius:18px;
          padding:1rem;
          background: var(--surface2);
          box-shadow: 0 16px 55px var(--shadow2);
        }
        .brief-title{ font-weight:980; letter-spacing:-.02em; color: var(--ink); }
        .brief-list{
          margin:.6rem 0 .85rem;
          padding-left:1.1rem;
          color: var(--muted);
          line-height:1.65;
          font-weight: 900;
        }
        .brief-note{
          border-top:1px dashed rgba(255,255,255,.22);
          padding-top:.75rem;
          color: var(--muted);
          line-height:1.65;
          font-weight: 850;
        }
        .note-strong{ font-weight:980; color: var(--ink); }
        .brief-mini{ margin-top:.85rem; display:grid; grid-template-columns:1fr 1fr; gap:.65rem; }
        .mini{ border:1px solid var(--border); border-radius:14px; padding:.75rem; background: rgba(255,255,255,.03); }
        .mini-k{ font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; font-weight:950; color: var(--subtle); }
        .mini-v{ margin-top:.2rem; font-weight:950; color: var(--muted); }
        .brief-intel{ margin-top:.9rem; border-top:1px dashed rgba(255,255,255,.22); padding-top:.75rem; }
        .brief-intel ul{ margin:.5rem 0 0; padding-left:1.1rem; color: var(--muted); font-weight:900; line-height:1.65; }
      
        /* Panels */
        .main{ margin-top:1rem; display:grid; gap:1rem; }
        .panel{
          border:1px solid var(--border);
          border-radius:22px;
          padding:1.25rem;
          background: var(--panel);
          box-shadow: 0 18px 58px var(--shadow);
        }
        .panel.emphasis{ background: var(--surface2); }
        .panel-title{ margin:0 0 .45rem; font-size:1.6rem; letter-spacing:-.02em; font-weight:995; color: var(--ink); }
        .panel-sub{ margin:0; color: var(--muted); line-height:1.75; font-size:1.06rem; font-weight: 900; max-width:95ch; }
      
        .grid-3{ margin-top:1rem; display:grid; grid-template-columns: repeat(auto-fit,minmax(240px,1fr)); gap:.85rem; }
      
        .card,.principle,.door{ border:1px solid var(--border); border-radius:20px; background: rgba(255,255,255,.03); }
        .card{ padding:1rem; }
        .card-title{ font-weight:995; letter-spacing:-.02em; margin-bottom:.35rem; color: var(--ink); }
        .card-body{ margin:0; color: var(--muted); line-height:1.75; font-weight: 900; }
        .card-links{ margin-top:.85rem; display:flex; flex-wrap:wrap; gap:.5rem; }
      
        .chip{
          display:inline-flex; align-items:center; justify-content:center;
          border-radius:999px;
          border:1px solid var(--border2);
          padding:.35rem .65rem;
          background: rgba(245,158,11,.10);
          color: var(--ink);
          font-weight:950;
          text-decoration:none;
          cursor:pointer;
        }
        .chip:hover{ background: rgba(245,158,11,.16); }
      
        .principles{ margin-top:1rem; display:grid; gap:.75rem; }
        .principle{ padding:1rem; display:grid; gap:.3rem; }
        .p-k{ font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; font-weight:950; color: var(--subtle); }
        .p-v{ color: var(--muted); line-height:1.75; font-size:1.06rem; font-weight: 900; }
      
        /* Doors */
        .doors{ margin-top:1rem; display:grid; grid-template-columns: repeat(auto-fit,minmax(290px,1fr)); gap:.9rem; }
        .door{
          display:block; text-decoration:none; padding:1.05rem; color: var(--ink);
          transition: transform 140ms ease, background 140ms ease, border-color 140ms ease, box-shadow 140ms ease;
        }
        .door:hover{
          transform: translateY(-3px);
          background: rgba(255,255,255,.06);
          border-color: rgba(255,255,255,.22);
          box-shadow: 0 18px 55px rgba(0,0,0,.28);
        }
        .door-eyebrow{ font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; font-weight:950; color: var(--subtle); margin-bottom:.35rem; }
        .door-title{ font-size:1.3rem; font-weight:995; letter-spacing:-.02em; margin-bottom:.35rem; color: var(--ink); }
        .door-desc{ color: var(--muted); line-height:1.7; margin-bottom:.75rem; font-weight: 900; }
        .door-bullets{ margin:0 0 .9rem; padding-left:1.1rem; color: var(--muted); line-height:1.7; font-weight: 900; }
        .door-cta{ display:flex; align-items:center; justify-content:space-between; border-top:1px dashed rgba(255,255,255,.22); padding-top:.75rem; font-weight:995; color: var(--ink); }
      
        /* New: Steps + Quick moves */
        .steps{ margin-top:1rem; display:grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap:.75rem; }
        .step{
          border:1px solid var(--border);
          border-radius:18px;
          padding:1rem;
          background: rgba(255,255,255,.03);
        }
        .step-k{ font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; font-weight:950; color: var(--subtle); }
        .step-v{ margin-top:.35rem; font-weight:995; color: var(--ink); }
        .step-s{ margin-top:.25rem; color: var(--muted); font-weight:900; line-height:1.6; }
      
        .quickMoves{ margin-top:1.1rem; border-top:1px dashed rgba(255,255,255,.22); padding-top:1rem; }
        .qm-title{ font-weight:995; color: var(--ink); margin-bottom:.65rem; }
        .qm-grid{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:.75rem; }
        .qm{
          border:1px solid var(--border);
          border-radius:18px;
          padding:1rem;
          text-decoration:none;
          background: linear-gradient(90deg, rgba(245,158,11,.12), rgba(96,165,250,.10), rgba(167,139,250,.10));
          color: var(--ink);
          transition: transform 120ms ease, border-color 120ms ease, background 120ms ease;
        }
        .qm:hover{ transform: translateY(-2px); border-color: rgba(255,255,255,.22); background: rgba(255,255,255,.06); }
        .qm-l{ font-weight:995; }
        .qm-n{ margin-top:.25rem; color: var(--muted); font-weight:900; line-height:1.6; }
      
        /* Closing */
        .closing{
          background: linear-gradient(180deg, rgba(245,158,11,.18), rgba(96,165,250,.12), rgba(167,139,250,.10), var(--panel));
        }
        .closing-inner{ max-width:95ch; }
        .closing-title{ margin:0 0 .4rem; font-size:1.75rem; font-weight:995; letter-spacing:-.02em; color: var(--ink); }
        .closing-body{ margin:0; color: var(--muted); line-height:1.8; font-size:1.12rem; font-weight: 950; }
        .closing-actions{ margin-top:1rem; display:flex; flex-wrap:wrap; gap:.75rem; }
        .fineprint{ margin-top:1rem; color: var(--subtle); line-height:1.65; font-size:.98rem; font-weight: 900; }
      
        /* Command palette */
        .paletteOverlay{
          position:fixed; inset:0; z-index:999;
          background: rgba(0,0,0,.55);
          backdrop-filter: blur(10px);
          display:grid; place-items:center;
          padding:1rem;
        }
        .palette{
          width:min(760px,96vw);
          border-radius:20px;
          border:1px solid var(--border2);
          background: rgba(11,18,32,.92);
          box-shadow: 0 40px 120px rgba(0,0,0,.70);
          overflow:hidden;
        }
        .paletteTop{ display:flex; align-items:center; justify-content:space-between; padding:.9rem 1rem; border-bottom:1px solid rgba(255,255,255,.10); }
        .paletteTitle{ font-weight:995; letter-spacing:-.02em; color: var(--ink); }
        .paletteClose{
          border:1px solid var(--border2);
          background: rgba(255,255,255,.04);
          color: var(--ink);
          border-radius:999px;
          padding:.35rem .65rem;
          font-weight:950;
          cursor:pointer;
        }
        .paletteInput{
          width:100%; border:none; outline:none; background:transparent;
          color: var(--ink);
          padding:.95rem 1rem;
          font-size:1.05rem;
          font-weight:900;
        }
        .paletteInput::placeholder{ color: rgba(231,238,248,.60); }
        .paletteList{ max-height:52vh; overflow:auto; border-top:1px solid rgba(255,255,255,.08); }
        .paletteItem{
          width:100%;
          display:grid;
          grid-template-columns: 140px 1fr;
          align-items:center;
          gap:.8rem;
          padding:.85rem 1rem;
          border:none;
          background:transparent;
          color: var(--ink);
          cursor:pointer;
          text-align:left;
          border-bottom:1px solid rgba(255,255,255,.06);
        }
        .paletteItem:hover{ background: linear-gradient(90deg, rgba(245,158,11,.16), rgba(96,165,250,.10), rgba(167,139,250,.08)); }
        .paletteGroup{ font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; font-weight:950; color: var(--subtle); }
        .paletteLabel{ font-weight:950; color: var(--ink); }
        .paletteEmpty{ padding:1rem; color: var(--muted); font-weight:900; }
        .paletteFooter{ display:flex; align-items:center; gap:.6rem; padding:.75rem 1rem; border-top:1px solid rgba(255,255,255,.10); color: var(--muted); font-weight:900; }
        .sep{ opacity:.6; }
      
        /* Ultra-wide */
        @media (min-width: 1500px){
          .stage{ grid-template-columns: 420px minmax(0,1fr) 360px; }
          .content{ padding: 2.25rem 3.25rem; }
          .hero-grid{ grid-template-columns: 1.45fr .75fr; }
        }
        @media (min-width: 1800px){
          .stage{ grid-template-columns: 460px minmax(0,1fr) 400px; }
        }
      
        /* Responsive */
        @media (max-width:1180px){
          .stage{ grid-template-columns: 360px minmax(0,1fr); }
          .intel{ display:none; }
        }
        @media (max-width:980px){
          .stage{ grid-template-columns: 1fr; }
          .rail{ position:relative; height:auto; border-right:none; border-bottom:1px solid var(--border); }
          .content{ padding:1rem; }
          .hero-grid{ grid-template-columns: 1fr; }
          .brief-mini{ grid-template-columns: 1fr; }
        }
        @media (max-width:520px){
          .cta{ width:100%; }
          .paletteItem{ grid-template-columns:1fr; gap:.25rem; }
        }
      
        /* Reduced motion */
        @media (prefers-reduced-motion: reduce){
          .aurora{ transform:none !important; }
          .spotlight{ display:none; }
          .mode-btn,.rail-link,.cta,.door,.rail-cta,.intel-cta,.qm{ transition:none !important; }
        }
      </style>
        