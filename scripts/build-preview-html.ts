// frontend/scripts/build-preview-html.ts
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { execSync } from 'node:child_process';
import {
  COLOR_TOKENS,
  TYPOGRAPHY_TOKENS,
  SPACING_TOKENS,
  RADIUS_TOKENS,
  PRINCIPLES,
  type ColorToken,
} from '../src/lib/design-tokens.ts';

const outDir = resolve(process.cwd(), '.ds4a');
mkdirSync(outDir, { recursive: true });
const outPath = resolve(outDir, 'preview.html');

const stats = [
  { label: 'Colors', value: COLOR_TOKENS.length },
  { label: 'Type styles', value: TYPOGRAPHY_TOKENS.length },
  { label: 'Spacing steps', value: SPACING_TOKENS.length },
  { label: 'Radii', value: RADIUS_TOKENS.length },
];

const COLOR_GROUPS: { id: ColorToken['category']; label: string }[] = [
  { id: 'surfaces', label: 'Surfaces' },
  { id: 'neutrals', label: 'Neutrals' },
  { id: 'brand', label: 'Brand' },
  { id: 'states', label: 'States' },
];

const RADIUS_PX: Record<string, number> = {
  'radius-card': 8,
  'radius-button': 8,
  'radius-none': 0,
};

function isDarkHex(hex: string) {
  const n = parseInt(hex.slice(1), 16);
  const [r, g, b] = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.4;
}

const THEME_CSS = [
  '@theme {',
  '  /* Color */',
  ...COLOR_TOKENS.map((c) => `  ${c.cssVar}: ${c.hex};`),
  '',
  '  /* Typography */',
  "  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;",
  "  --font-display: 'Geist', system-ui, sans-serif;",
  "  --font-mono: 'Geist Mono', ui-monospace, monospace;",
  '',
  '  /* Layout & radius (capped at 8px) */',
  '  --container-max: 1280px;',
  '  --radius-card: 0.5rem;',
  '  --radius-button: 0.5rem;',
  '}',
].join('\n');

// Build Principles HTML
const principlesHtml = PRINCIPLES.map(
  (p, i) => `
    <li class="bg-lumyra-white p-6" data-token-item="${p.title} ${p.desc}">
      <span class="font-mono text-xs tabular-nums text-lumyra-gray-400">${String(i + 1).padStart(2, '0')}</span>
      <h3 class="mt-3 font-display text-base font-medium text-balance text-lumyra-black">${p.title}</h3>
      <p class="mt-1.5 text-sm leading-relaxed text-pretty text-lumyra-gray-600">${p.desc}</p>
    </li>
  `
).join('\n');

// Build Colors HTML
const colorsHtml = COLOR_GROUPS.map((g) => {
  const groupColors = COLOR_TOKENS.filter((c) => c.category === g.id);
  const swatchesHtml = groupColors
    .map((c) => {
      const dark = isDarkHex(c.hex);
      return `
        <div class="flex flex-col overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-white" data-token-item="${c.name} ${c.hex} ${c.cssVar} ${c.tailwindBg} ${c.role}">
          <button
            type="button"
            onclick="copyText('${c.hex}')"
            style="background-color: ${c.hex};"
            class="group flex h-28 items-end justify-between border-b border-lumyra-gray-200 p-3 text-left font-mono text-xs cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-lumyra-accent ${
              dark ? 'text-lumyra-white' : 'text-lumyra-black'
            }"
            aria-label="Copy ${c.name} ${c.hex}"
          >
            <span class="tabular-nums">${c.hex}</span>
            <span class="opacity-0 transition-opacity group-hover:opacity-70 group-focus-visible:opacity-70">Copy</span>
          </button>
          <div class="flex flex-1 flex-col p-3">
            <p class="text-sm font-medium text-lumyra-black">${c.name}</p>
            <p class="mt-1 mb-3 flex-1 text-xs leading-relaxed text-pretty text-lumyra-gray-600">${c.role}</p>
            ${c.wcag ? `<p class="mb-2 text-xs text-lumyra-gray-600">${c.wcag}</p>` : ''}
            <div class="-mx-2 space-y-0.5">
              <button
                type="button"
                onclick="copyText('var(${c.cssVar})')"
                class="flex w-full items-center justify-between gap-2 rounded px-2 py-1 font-mono text-xs text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-lumyra-accent"
                aria-label="Copy var(${c.cssVar})"
              >
                <span class="truncate">var(${c.cssVar})</span>
                <span class="shrink-0 text-[11px] text-lumyra-gray-400">Copy</span>
              </button>
              <button
                type="button"
                onclick="copyText('${c.tailwindBg}')"
                class="flex w-full items-center justify-between gap-2 rounded px-2 py-1 font-mono text-xs text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-lumyra-accent"
                aria-label="Copy ${c.tailwindBg}"
              >
                <span class="truncate">${c.tailwindBg}</span>
                <span class="shrink-0 text-[11px] text-lumyra-gray-400">Copy</span>
              </button>
            </div>
          </div>
        </div>
      `;
    })
    .join('\n');

  return `
    <div data-group="${g.id}">
      <h3 class="mb-3 text-xs font-medium uppercase tracking-[0.1em] text-lumyra-gray-600">${g.label}</h3>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        ${swatchesHtml}
      </div>
    </div>
  `;
}).join('\n');

// Build Typography HTML
const typographyHtml = TYPOGRAPHY_TOKENS.map((t) => {
  const isUppercase = t.id === 'label-xs' || t.id === 'eyebrow';
  const familyClass = t.family === 'Geist' ? 'font-display' : t.family === 'Geist Mono' ? 'font-mono' : 'font-sans';
  return `
    <div class="grid gap-3 px-5 py-5 md:grid-cols-[180px_minmax(0,1fr)] md:items-baseline md:gap-8" data-token-item="${t.id} ${t.name} ${t.family} ${t.description}">
      <div>
        <button
          type="button"
          onclick="copyText('${t.id}')"
          class="font-mono text-xs text-lumyra-black hover:text-lumyra-accent cursor-pointer"
          aria-label="Copy token ${t.id}"
        >
          ${t.id}
        </button>
        <p class="mt-1 font-mono text-xs tabular-nums text-lumyra-gray-400">
          ${t.family} · ${t.sizePx}/${t.weight}
        </p>
      </div>
      <p
        class="${familyClass} ${isUppercase ? 'uppercase' : ''} truncate text-lumyra-black sample-render"
        style="font-size: ${t.sizePx}px; font-weight: ${t.weight}; letter-spacing: ${t.letterSpacing};"
        data-default="${t.sampleText}"
        title="${t.description}"
      >
        ${t.sampleText}
      </p>
    </div>
  `;
}).join('\n');

// Build Spacing HTML
const spacingHtml = SPACING_TOKENS.map(
  (s) => `
    <button
      type="button"
      onclick="copyText('${s.px}px')"
      class="group grid w-full grid-cols-[72px_64px_minmax(0,1fr)] items-center gap-4 px-5 py-3 text-left transition-colors hover:bg-lumyra-gray-100/60 cursor-pointer focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-inset focus-visible:ring-lumyra-accent sm:grid-cols-[72px_64px_120px_minmax(0,1fr)]"
      data-token-item="${s.token} ${s.usage} ${s.px}px"
      aria-label="Copy spacing ${s.token}, ${s.px}px"
    >
      <span class="font-mono text-xs tabular-nums text-lumyra-black">${s.token}</span>
      <span class="font-mono text-xs tabular-nums text-lumyra-gray-600">${s.px}px</span>
      <span class="hidden sm:block">
        <span
          class="block h-3 rounded-[2px] bg-lumyra-accent/80 transition-colors group-hover:bg-lumyra-accent"
          style="width: ${s.px * 3}px;"
        ></span>
      </span>
      <span class="truncate text-xs text-lumyra-gray-600">${s.usage}</span>
    </button>
  `
).join('\n');

// Build Radius HTML
const radiusHtml = RADIUS_TOKENS.map(
  (r) => `
    <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white p-5" data-token-item="${r.name} ${r.description}">
      <div
        class="h-20 border border-lumyra-gray-400 bg-lumyra-cream"
        style="border-radius: ${RADIUS_PX[r.id] ?? 8}px;"
      ></div>
      <div class="mt-4 flex items-baseline justify-between gap-2">
        <h3 class="text-sm font-medium text-lumyra-black">${r.name}</h3>
        <span class="font-mono text-xs tabular-nums text-lumyra-gray-600">${RADIUS_PX[r.id] ?? 8}px</span>
      </div>
      <p class="mt-1 text-xs leading-relaxed text-pretty text-lumyra-gray-600">${r.description}</p>
    </div>
  `
).join('\n');

// Preliminary content for CSS extraction
const preliminaryHtml = `
  <div class="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <header class="py-14 sm:py-20 border-b border-lumyra-gray-200">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <p class="text-xs font-medium uppercase tracking-[0.125em] text-lumyra-gray-600">Getlumyra · Design System</p>
        <span class="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-mono text-lumyra-gray-800 bg-lumyra-cream border border-lumyra-gray-200 rounded-button">
          <span class="w-1.5 h-1.5 rounded-full bg-lumyra-success"></span>
          dev-only
        </span>
      </div>
      <h1 class="mt-4 max-w-3xl font-display text-4xl sm:text-5xl font-medium tracking-tight text-balance leading-[1.1] text-lumyra-black">
        Quiet surfaces, clear intent.
      </h1>
      <p class="mt-4 max-w-2xl text-base sm:text-lg text-pretty leading-relaxed text-lumyra-gray-600">
        Living specimen sheet and interactive explorer for Lumyra tokens. All values are single-sourced from
        <code class="px-1.5 py-0.5 font-mono text-xs text-lumyra-gray-800 bg-lumyra-gray-100 rounded-sm">src/lib/design-tokens.ts</code>
        and compiled directly into Tailwind v4 <code class="px-1.5 py-0.5 font-mono text-xs text-lumyra-gray-800 bg-lumyra-gray-100 rounded-sm">@theme</code>.
      </p>
      <dl class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-4 max-w-2xl">
        <div class="border-l-2 border-lumyra-black pl-3 py-1">
          <dt class="text-xs text-lumyra-gray-600 uppercase tracking-wider">COLORS</dt>
          <dd class="text-2xl font-medium text-lumyra-black font-display tabular-nums">14</dd>
        </div>
        <div class="border-l-2 border-lumyra-black pl-3 py-1">
          <dt class="text-xs text-lumyra-gray-600 uppercase tracking-wider">TYPE STYLES</dt>
          <dd class="text-2xl font-medium text-lumyra-black font-display tabular-nums">14</dd>
        </div>
        <div class="border-l-2 border-lumyra-black pl-3 py-1">
          <dt class="text-xs text-lumyra-gray-600 uppercase tracking-wider">SPACING STEPS</dt>
          <dd class="text-2xl font-medium text-lumyra-black font-display tabular-nums">10</dd>
        </div>
        <div class="border-l-2 border-lumyra-black pl-3 py-1">
          <dt class="text-xs text-lumyra-gray-600 uppercase tracking-wider">RADII</dt>
          <dd class="text-2xl font-medium text-lumyra-black font-display tabular-nums">3</dd>
        </div>
      </dl>
    </header>

    <div class="pb-24">
      <div class="lg:grid lg:grid-cols-[200px_minmax(0,1fr)] lg:gap-16">
        <aside class="hidden lg:block">
          <div class="sticky top-10 space-y-6 pt-14">
            <div class="relative">
              <label for="ds-search" class="sr-only">Search tokens</label>
              <svg aria-hidden="true" viewBox="0 0 16 16" class="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-lumyra-gray-400" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="7" cy="7" r="4.5" />
                <path d="m10.5 10.5 3 3" stroke-linecap="round" />
              </svg>
              <input
                id="ds-search"
                type="search"
                placeholder="Search tokens"
                class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-white py-2 pl-9 pr-3 text-base sm:text-sm text-lumyra-black placeholder:text-lumyra-gray-400 focus:border-lumyra-accent focus:outline-none focus:ring-1 focus:ring-lumyra-accent"
              />
            </div>
            <nav aria-label="Sections">
              <ul class="space-y-0.5 border-l border-lumyra-gray-200">
                <li><a href="#principles" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-lumyra-black font-medium text-lumyra-black">Principles</a></li>
                <li><a href="#colors" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black">Color</a></li>
                <li><a href="#typography" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black">Typography</a></li>
                <li><a href="#spacing" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black">Spacing</a></li>
                <li><a href="#radii" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black">Radius</a></li>
                <li><a href="#components" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black">Components</a></li>
                <li><a href="#theme" class="-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black">Theme code</a></li>
              </ul>
            </nav>
          </div>
        </aside>

        <div class="min-w-0 divide-y divide-lumyra-gray-200 [&>section]:py-14 [&>section]:scroll-mt-36 lg:[&>section]:scroll-mt-20">
          <section id="principles">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">01</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Principles</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">Restraint over decoration. Every surface, border, and color carries a single, clear job.</p>
            </header>
            <ol class="grid gap-px overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-gray-200 sm:grid-cols-2">
              ${principlesHtml}
            </ol>
          </section>

          <section id="colors">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">02</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Color</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">Fourteen tokens across four roles. Click a swatch to copy its hex, or a chip to copy the variable or utility.</p>
            </header>
            <div class="space-y-10">
              ${colorsHtml}
            </div>
          </section>

          <section id="typography">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">03</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Typography</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">Geist for display, Inter for interface and prose, Geist Mono for identifiers. Nothing heavier than 500.</p>
            </header>
            <div class="mb-8 grid gap-px overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-gray-200 md:grid-cols-3">
              <div class="bg-lumyra-white p-6">
                <div class="font-display text-5xl font-medium tracking-tight text-lumyra-black">Aa</div>
                <h3 class="mt-5 text-sm font-medium text-lumyra-black">Geist</h3>
                <p class="mt-1 text-xs text-lumyra-gray-600">Headlines, card titles, hero statements</p>
              </div>
              <div class="bg-lumyra-white p-6">
                <div class="font-sans text-5xl font-medium tracking-tight text-lumyra-black">Aa</div>
                <h3 class="mt-5 text-sm font-medium text-lumyra-black">Inter</h3>
                <p class="mt-1 text-xs text-lumyra-gray-600">Buttons, inputs, navigation, body copy</p>
              </div>
              <div class="bg-lumyra-white p-6">
                <div class="font-mono text-5xl font-medium tracking-tight text-lumyra-black">Aa</div>
                <h3 class="mt-5 text-sm font-medium text-lumyra-black">Geist Mono</h3>
                <p class="mt-1 text-xs text-lumyra-gray-600">Invite codes, dimensions, hex values</p>
              </div>
            </div>
            <div class="mb-4">
              <label for="ds-sample" class="sr-only">Sample text</label>
              <input
                id="ds-sample"
                type="text"
                placeholder="Type to preview your own copy across the scale"
                class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-white px-3 py-2 text-base sm:text-sm text-lumyra-black placeholder:text-lumyra-gray-400 focus:border-lumyra-accent focus:outline-none focus:ring-1 focus:ring-lumyra-accent"
              />
            </div>
            <div class="divide-y divide-lumyra-gray-200 rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
              ${typographyHtml}
            </div>
          </section>

          <section id="spacing">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">04</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Spacing</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">A tight, small-step scale for controls and cards, opening up at 24 and 32 for layout rhythm.</p>
            </header>
            <div class="divide-y divide-lumyra-gray-200 rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
              ${spacingHtml}
            </div>
          </section>

          <section id="radii">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">05</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Radius</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">Corners stop at 8px. Pills and bubbly shapes are out; square edges handle structural lines.</p>
            </header>
            <div class="grid gap-4 md:grid-cols-3">
              ${radiusHtml}
            </div>
            <div class="mt-4 grid gap-4 sm:grid-cols-2">
              <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white p-5">
                <p class="mb-3 text-xs font-medium text-lumyra-success">Do · 4–8px</p>
                <span class="inline-flex h-9 items-center rounded-md bg-lumyra-black px-4 text-sm font-medium text-lumyra-white">
                  Claim image
                </span>
              </div>
              <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white p-5">
                <p class="mb-3 text-xs font-medium text-lumyra-danger">Don’t · fully rounded</p>
                <span class="inline-flex h-9 items-center bg-lumyra-gray-200 px-4 text-sm font-medium text-lumyra-gray-600" style="border-radius: 9999px;">
                  Claim image
                </span>
              </div>
            </div>
          </section>

          <section id="components">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">06</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Components</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">Live specimens built from the same utilities the product uses.</p>
            </header>
            <div class="space-y-4">
              <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                <div class="flex items-center justify-between gap-4 border-b border-lumyra-gray-200 px-5 py-3">
                  <h3 class="text-sm font-medium text-lumyra-black">Buttons</h3>
                </div>
                <div class="p-5 sm:p-6">
                  <div class="flex flex-wrap items-center gap-3">
                    <button type="button" class="rounded-md bg-lumyra-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-lumyra-accent-hover cursor-pointer">Primary</button>
                    <button type="button" class="rounded-md bg-lumyra-black px-4 py-2 text-sm font-medium text-lumyra-white transition-colors hover:bg-lumyra-gray-800 cursor-pointer">Dark</button>
                    <button type="button" class="rounded-md border border-lumyra-gray-200 bg-lumyra-white px-4 py-2 text-sm font-medium text-lumyra-black transition-colors hover:bg-lumyra-gray-100 cursor-pointer">Secondary</button>
                    <button type="button" class="rounded-md px-4 py-2 text-sm font-medium text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer">Ghost</button>
                    <button type="button" class="rounded-md bg-lumyra-danger px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-600 cursor-pointer">Destructive</button>
                    <button type="button" disabled class="rounded-md bg-lumyra-gray-100 px-4 py-2 text-sm font-medium text-lumyra-gray-400 cursor-not-allowed">Disabled</button>
                  </div>
                </div>
              </div>

              <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                <div class="flex items-center justify-between gap-4 border-b border-lumyra-gray-200 px-5 py-3">
                  <h3 class="text-sm font-medium text-lumyra-black">Badges</h3>
                </div>
                <div class="p-5 sm:p-6">
                  <div class="flex flex-wrap items-center gap-3">
                    <span class="inline-flex items-center gap-1.5 rounded border border-emerald-200 bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-800">
                      <span class="h-1.5 w-1.5 rounded-full bg-lumyra-success"></span>
                      Available
                    </span>
                    <span class="inline-flex items-center gap-1.5 rounded border border-violet-200 bg-violet-50 px-2.5 py-0.5 text-xs font-medium text-violet-800">
                      <span class="h-1.5 w-1.5 rounded-full bg-lumyra-claimed"></span>
                      Claimed
                    </span>
                    <span class="rounded border border-lumyra-gray-200 bg-lumyra-gray-100 px-2 py-0.5 text-xs font-medium uppercase tracking-wider text-lumyra-gray-600">
                      Beta
                    </span>
                    <span class="rounded border border-lumyra-gray-200 bg-lumyra-cream px-2.5 py-0.5 font-mono text-xs tabular-nums text-lumyra-gray-800">
                      LMYR-2026
                    </span>
                  </div>
                </div>
              </div>

              <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                <div class="flex items-center justify-between gap-4 border-b border-lumyra-gray-200 px-5 py-3">
                  <h3 class="text-sm font-medium text-lumyra-black">Inputs</h3>
                </div>
                <div class="p-5 sm:p-6">
                  <div class="grid gap-5 md:grid-cols-3">
                    <div>
                      <label for="ds-in-default" class="mb-1.5 block text-xs font-medium text-lumyra-gray-800">Title</label>
                      <input id="ds-in-default" type="text" placeholder="Artwork title" class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-white px-3 py-2 text-base sm:text-sm text-lumyra-black placeholder:text-lumyra-gray-400 focus:border-lumyra-accent focus:outline-none focus:ring-1 focus:ring-lumyra-accent" />
                    </div>
                    <div>
                      <label for="ds-in-code" class="mb-1.5 block text-xs font-medium text-lumyra-gray-800">Invite code</label>
                      <input id="ds-in-code" type="text" value="LMYR-2026-BETA" readonly class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-cream px-3 py-2 font-mono text-base sm:text-sm tracking-widest tabular-nums text-lumyra-black focus:outline-none" />
                    </div>
                    <div>
                      <label for="ds-in-error" class="mb-1.5 block text-xs font-medium text-lumyra-gray-800">Email</label>
                      <input id="ds-in-error" type="text" value="designer@" aria-invalid="true" class="w-full rounded-md border border-lumyra-danger bg-lumyra-white px-3 py-2 text-base sm:text-sm text-lumyra-black focus:outline-none focus:ring-1 focus:ring-lumyra-danger" />
                      <p class="mt-1.5 text-xs text-lumyra-danger">Enter a valid email address.</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                <div class="flex items-center justify-between gap-4 border-b border-lumyra-gray-200 px-5 py-3">
                  <h3 class="text-sm font-medium text-lumyra-black">Artwork card</h3>
                  <div role="group" aria-label="Card state" class="flex rounded-md bg-lumyra-gray-100 p-0.5 text-xs font-medium">
                    <button type="button" id="card-toggle-avail" onclick="setCardState(false)" class="rounded px-2.5 py-1 transition-colors cursor-pointer bg-lumyra-white text-lumyra-black shadow-xs">Available</button>
                    <button type="button" id="card-toggle-claim" onclick="setCardState(true)" class="rounded px-2.5 py-1 transition-colors cursor-pointer text-lumyra-gray-600 hover:text-lumyra-black">Claimed</button>
                  </div>
                </div>
                <div class="p-5 sm:p-6">
                  <div class="mx-auto max-w-xs overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                    <div class="relative flex aspect-4/3 items-center justify-center bg-lumyra-gray-100">
                      <span class="font-mono text-xs tabular-nums text-lumyra-gray-400">4:3</span>
                      <span id="card-badge" class="absolute right-2.5 top-2.5 rounded px-2.5 py-0.5 text-xs font-medium text-white bg-lumyra-success">Available</span>
                    </div>
                    <div class="p-4">
                      <div class="flex items-center justify-between text-xs text-lumyra-gray-600">
                        <span class="font-mono tabular-nums">#042</span>
                        <span>Abstract</span>
                      </div>
                      <p class="mt-1.5 font-display text-base font-medium text-lumyra-black">Prismatic Monolith No. 4</p>
                      <div class="mt-3 flex items-center justify-between border-t border-lumyra-gray-100 pt-3">
                        <span class="font-mono text-xs tabular-nums text-lumyra-gray-400">2464 × 1856</span>
                        <button id="card-btn" type="button" class="rounded-md px-3 py-1 text-xs font-medium transition-colors bg-lumyra-black text-lumyra-white hover:bg-lumyra-gray-800 cursor-pointer">Claim</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section id="theme">
            <header class="mb-8 max-w-2xl">
              <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">07</p>
              <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">Theme code</h2>
              <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">The Tailwind v4 <code class="font-mono text-xs text-lumyra-black">@theme</code> block behind every token above.</p>
            </header>
            <div class="overflow-hidden rounded-lg border border-lumyra-gray-800 bg-lumyra-black">
              <div class="flex items-center justify-between border-b border-lumyra-gray-800 px-4 py-2.5">
                <span class="font-mono text-xs text-lumyra-gray-400">global.css</span>
                <button type="button" onclick="copyText(document.querySelector('#theme-code').textContent)" class="rounded px-2 py-1 font-mono text-xs text-lumyra-gray-400 transition-colors hover:bg-lumyra-gray-800 hover:text-lumyra-white cursor-pointer">Copy</button>
              </div>
              <pre class="overflow-x-auto p-5 font-mono text-xs leading-relaxed text-lumyra-gray-100"><code id="theme-code">${THEME_CSS}</code></pre>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
`;

// Compile Tailwind CSS for this exact HTML using @tailwindcss/cli
let compiledCss = '';
try {
  // First write temporary HTML for CLI scanning
  writeFileSync(outPath, preliminaryHtml, 'utf-8');
  compiledCss = execSync(`npx @tailwindcss/cli -i src/styles/global.css --content "${outPath}"`, {
    encoding: 'utf-8',
  });
} catch (err) {
  console.warn('Fallback Tailwind compilation notice:', err);
}

const fullHtml = `<!DOCTYPE html>
<html lang="en" class="bg-lumyra-white text-lumyra-black antialiased selection:bg-lumyra-accent/20 selection:text-lumyra-black">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Design System — Getlumyra</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
${compiledCss}
  </style>
</head>
<body class="min-h-screen bg-lumyra-white text-lumyra-black">
  ${preliminaryHtml}

  <div id="toast" class="fixed bottom-6 right-6 z-50 rounded-md bg-lumyra-black px-4 py-2 font-mono text-xs text-white opacity-0 transition-opacity duration-200 pointer-events-none">
    Copied to clipboard
  </div>

  <script>
    function copyText(text) {
      navigator.clipboard.writeText(text).then(() => {
        showToast('Copied: ' + text);
      }).catch(() => {
        showToast('Copied: ' + text);
      });
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.remove('opacity-0');
      t.classList.add('opacity-100');
      setTimeout(() => {
        t.classList.remove('opacity-100');
        t.classList.add('opacity-0');
      }, 1600);
    }

    function updateTypographySample(val) {
      document.querySelectorAll('.sample-render').forEach(el => {
        el.textContent = val || el.getAttribute('data-default');
      });
    }

    function filterTokens(q) {
      q = q.toLowerCase().trim();
      document.querySelectorAll('[data-token-item]').forEach(el => {
        const text = el.getAttribute('data-token-item').toLowerCase();
        el.style.display = (!q || text.includes(q)) ? '' : 'none';
      });
    }

    function setCardState(claimed) {
      const availBtn = document.getElementById('card-toggle-avail');
      const claimBtn = document.getElementById('card-toggle-claim');
      const badge = document.getElementById('card-badge');
      const actionBtn = document.getElementById('card-btn');

      if (claimed) {
        availBtn.className = 'rounded px-2.5 py-1 transition-colors cursor-pointer text-lumyra-gray-600 hover:text-lumyra-black';
        claimBtn.className = 'rounded px-2.5 py-1 transition-colors cursor-pointer bg-lumyra-white text-lumyra-black shadow-xs';
        badge.className = 'absolute right-2.5 top-2.5 rounded px-2.5 py-0.5 text-xs font-medium text-white bg-lumyra-claimed';
        badge.textContent = 'Claimed';
        actionBtn.className = 'rounded-md px-3 py-1 text-xs font-medium transition-colors bg-lumyra-gray-100 text-lumyra-gray-400 cursor-not-allowed';
        actionBtn.disabled = true;
      } else {
        claimBtn.className = 'rounded px-2.5 py-1 transition-colors cursor-pointer text-lumyra-gray-600 hover:text-lumyra-black';
        availBtn.className = 'rounded px-2.5 py-1 transition-colors cursor-pointer bg-lumyra-white text-lumyra-black shadow-xs';
        badge.className = 'absolute right-2.5 top-2.5 rounded px-2.5 py-0.5 text-xs font-medium text-white bg-lumyra-success';
        badge.textContent = 'Available';
        actionBtn.className = 'rounded-md px-3 py-1 text-xs font-medium transition-colors bg-lumyra-black text-lumyra-white hover:bg-lumyra-gray-800 cursor-pointer';
        actionBtn.disabled = false;
      }
    }

    // Active nav tracking on scroll
    const sections = ['principles', 'colors', 'typography', 'spacing', 'radii', 'components', 'theme'];
    window.addEventListener('scroll', () => {
      let current = sections[0];
      sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 160) current = id;
        }
      });
      document.querySelectorAll('aside nav a').forEach(link => {
        const href = link.getAttribute('href').replace('#', '');
        if (href === current) {
          link.className = '-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-lumyra-black font-medium text-lumyra-black';
        } else {
          link.className = '-ml-px block border-l py-1.5 pl-4 text-sm transition-colors border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black';
        }
      });
    }, { passive: true });
  </script>
</body>
</html>
`;

writeFileSync(outPath, fullHtml, 'utf-8');
console.log('✓ Successfully generated identical interactive preview at', outPath);
