// frontend/scripts/build-preview-html.ts
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
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

const SECTIONS = [
  { id: 'principles', label: 'Principles' },
  { id: 'colors', label: 'Color' },
  { id: 'typography', label: 'Typography' },
  { id: 'spacing', label: 'Spacing' },
  { id: 'radii', label: 'Radius' },
  { id: 'components', label: 'Components' },
  { id: 'theme', label: 'Theme code' },
] as const;

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
            class="group flex h-28 items-end justify-between border-b border-lumyra-gray-200 p-3 text-left font-mono text-xs cursor-pointer focus-visible:outline-none ${
              dark ? 'text-lumyra-white' : 'text-lumyra-black'
            }"
            aria-label="Copy ${c.name} ${c.hex}"
          >
            <span class="tabular-nums">${c.hex}</span>
            <span class="opacity-0 transition-opacity group-hover:opacity-70 text-[11px]">Copy</span>
          </button>
          <div class="flex flex-1 flex-col p-3">
            <p class="text-sm font-medium text-lumyra-black">${c.name}</p>
            <p class="mt-1 mb-3 flex-1 text-xs leading-relaxed text-pretty text-lumyra-gray-600">${c.role}</p>
            ${c.wcag ? `<p class="mb-2 text-xs text-lumyra-gray-600">${c.wcag}</p>` : ''}
            <div class="-mx-2 space-y-0.5">
              <button
                type="button"
                onclick="copyText('var(${c.cssVar})')"
                class="flex w-full items-center justify-between gap-2 rounded px-2 py-1 font-mono text-xs text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer"
              >
                <span class="truncate">var(${c.cssVar})</span>
                <span class="shrink-0 text-[11px] text-lumyra-gray-400 copy-status">Copy</span>
              </button>
              <button
                type="button"
                onclick="copyText('${c.tailwindBg}')"
                class="flex w-full items-center justify-between gap-2 rounded px-2 py-1 font-mono text-xs text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer"
              >
                <span class="truncate">${c.tailwindBg}</span>
                <span class="shrink-0 text-[11px] text-lumyra-gray-400 copy-status">Copy</span>
              </button>
            </div>
          </div>
        </div>
      `;
    })
    .join('\n');

  return `
    <div class="color-group mb-10" data-group="${g.id}">
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
    <div class="grid gap-3 px-5 py-5 md:grid-cols-[180px_minmax(0,1fr)] md:items-baseline md:gap-8 typography-row" data-token-item="${t.id} ${t.name} ${t.family} ${t.description}">
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
      class="group grid w-full grid-cols-[72px_64px_minmax(0,1fr)] items-center gap-4 px-5 py-3 text-left transition-colors hover:bg-lumyra-gray-100/60 cursor-pointer sm:grid-cols-[72px_64px_120px_minmax(0,1fr)] spacing-row"
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

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Design System — Getlumyra</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --color-lumyra-white: #fafaf9;
      --color-lumyra-cream: #f5f0e8;
      --color-lumyra-gray-100: #f4f4f5;
      --color-lumyra-black: #0a0a0a;
      --color-lumyra-gray-800: #27272a;
      --color-lumyra-gray-600: #52525b;
      --color-lumyra-gray-400: #a1a1aa;
      --color-lumyra-gray-200: #e4e4e7;
      --color-lumyra-accent: #6366f1;
      --color-lumyra-accent-hover: #4f46e5;
      --color-lumyra-claimed: #8b5cf6;
      --color-lumyra-success: #10b981;
      --color-lumyra-warning: #f59e0b;
      --color-lumyra-danger: #ef4444;
      --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
      --font-display: 'Geist', system-ui, sans-serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
      --radius-card: 0.5rem;
      --radius-button: 0.5rem;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      background-color: var(--color-lumyra-white);
      color: var(--color-lumyra-black);
      font-family: var(--font-sans);
      font-size: 14px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }

    /* Layout & container */
    .container {
      width: 100%;
      max-width: 80rem; /* 1280px */
      margin-left: auto;
      margin-right: auto;
      padding-left: 1rem;
      padding-right: 1rem;
    }
    @media (min-width: 640px) { .container { padding-left: 1.5rem; padding-right: 1.5rem; } }
    @media (min-width: 1024px) { .container { padding-left: 2rem; padding-right: 2rem; } }

    /* Utility typography */
    .font-sans { font-family: var(--font-sans); }
    .font-display { font-family: var(--font-display); }
    .font-mono { font-family: var(--font-mono); }
    .tabular-nums { font-variant-numeric: tabular-nums; }
    .text-balance { text-wrap: balance; }
    .text-pretty { text-wrap: pretty; }
    .truncate { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .uppercase { text-transform: uppercase; }

    /* Colors */
    .bg-lumyra-white { background-color: var(--color-lumyra-white); }
    .bg-lumyra-cream { background-color: var(--color-lumyra-cream); }
    .bg-lumyra-black { background-color: var(--color-lumyra-black); }
    .bg-lumyra-gray-100 { background-color: var(--color-lumyra-gray-100); }
    .bg-lumyra-gray-200 { background-color: var(--color-lumyra-gray-200); }
    .bg-lumyra-accent { background-color: var(--color-lumyra-accent); }
    .bg-lumyra-success { background-color: var(--color-lumyra-success); }
    .bg-lumyra-claimed { background-color: var(--color-lumyra-claimed); }
    .bg-lumyra-danger { background-color: var(--color-lumyra-danger); }

    .text-lumyra-black { color: var(--color-lumyra-black); }
    .text-lumyra-white { color: var(--color-lumyra-white); }
    .text-lumyra-gray-800 { color: var(--color-lumyra-gray-800); }
    .text-lumyra-gray-600 { color: var(--color-lumyra-gray-600); }
    .text-lumyra-gray-400 { color: var(--color-lumyra-gray-400); }
    .text-lumyra-accent { color: var(--color-lumyra-accent); }
    .text-lumyra-success { color: var(--color-lumyra-success); }
    .text-lumyra-danger { color: var(--color-lumyra-danger); }

    .border-lumyra-gray-100 { border-color: var(--color-lumyra-gray-100); }
    .border-lumyra-gray-200 { border-color: var(--color-lumyra-gray-200); }
    .border-lumyra-gray-400 { border-color: var(--color-lumyra-gray-400); }
    .border-lumyra-black { border-color: var(--color-lumyra-black); }
    .border-lumyra-accent { border-color: var(--color-lumyra-accent); }
    .border-lumyra-danger { border-color: var(--color-lumyra-danger); }

    /* Header */
    header.hero {
      padding-top: 3.5rem;
      padding-bottom: 3.5rem;
      border-bottom: 1px solid var(--color-lumyra-gray-200);
    }
    @media (min-width: 640px) { header.hero { padding-top: 5rem; padding-bottom: 5rem; } }

    .kicker-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
    }
    .kicker {
      font-size: 0.75rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.125em;
      color: var(--color-lumyra-gray-600);
    }
    .dev-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.375rem;
      padding: 0.25rem 0.625rem;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      color: var(--color-lumyra-gray-800);
      background-color: var(--color-lumyra-cream);
      border: 1px solid var(--color-lumyra-gray-200);
      border-radius: var(--radius-button);
    }
    .dev-dot {
      width: 0.375rem;
      height: 0.375rem;
      border-radius: 9999px;
      background-color: var(--color-lumyra-success);
    }

    h1.hero-title {
      margin-top: 1rem;
      max-width: 48rem;
      font-family: var(--font-display);
      font-size: 2.25rem;
      line-height: 1.1;
      font-weight: 500;
      letter-spacing: -0.025em;
      color: var(--color-lumyra-black);
    }
    @media (min-width: 640px) { h1.hero-title { font-size: 3rem; } }

    p.hero-desc {
      margin-top: 1rem;
      max-width: 42rem;
      font-size: 1rem;
      line-height: 1.625;
      color: var(--color-lumyra-gray-600);
    }
    @media (min-width: 640px) { p.hero-desc { font-size: 1.125rem; } }

    code.inline-code {
      padding: 0.125rem 0.375rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--color-lumyra-gray-800);
      background-color: var(--color-lumyra-gray-100);
      border-radius: 0.125rem;
    }

    /* Stats DL */
    dl.stats-grid {
      margin-top: 2rem;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 1rem;
      max-width: 42rem;
    }
    @media (min-width: 640px) { dl.stats-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }

    .stat-box {
      border-left: 2px solid var(--color-lumyra-black);
      padding-left: 0.75rem;
      padding-top: 0.25rem;
      padding-bottom: 0.25rem;
    }
    .stat-label {
      font-size: 0.75rem;
      color: var(--color-lumyra-gray-600);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .stat-value {
      font-size: 1.5rem;
      font-weight: 500;
      color: var(--color-lumyra-black);
      font-family: var(--font-display);
    }

    /* 2-column Body Layout */
    .explorer-layout {
      padding-bottom: 6rem;
    }
    @media (min-width: 1024px) {
      .explorer-grid {
        display: grid;
        grid-template-columns: 200px minmax(0, 1fr);
        gap: 4rem;
      }
    }

    /* Sidebar */
    .sidebar {
      display: none;
    }
    @media (min-width: 1024px) {
      .sidebar {
        display: block;
      }
    }
    .sidebar-sticky {
      position: sticky;
      top: 6rem;
      padding-top: 3.5rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .search-wrap {
      position: relative;
    }
    .search-icon {
      pointer-events: none;
      position: absolute;
      left: 0.75rem;
      top: 50%;
      transform: translateY(-50%);
      width: 0.875rem;
      height: 0.875rem;
      color: var(--color-lumyra-gray-400);
    }
    input.search-input {
      width: 100%;
      border-radius: 0.375rem;
      border: 1px solid var(--color-lumyra-gray-200);
      background-color: var(--color-lumyra-white);
      padding: 0.5rem 0.75rem 0.5rem 2.25rem;
      font-size: 0.875rem;
      color: var(--color-lumyra-black);
    }
    input.search-input:focus {
      outline: 2px solid var(--color-lumyra-accent);
      outline-offset: -1px;
    }

    /* Sidebar Nav */
    ul.sidebar-nav {
      list-style: none;
      border-left: 1px solid var(--color-lumyra-gray-200);
      display: flex;
      flex-direction: column;
      gap: 0.125rem;
    }
    .sidebar-link {
      display: block;
      margin-left: -1px;
      border-left: 1px solid transparent;
      padding: 0.375rem 0 0.375rem 1rem;
      font-size: 0.875rem;
      color: var(--color-lumyra-gray-600);
      text-decoration: none;
      transition: color 0.15s, border-color 0.15s;
    }
    .sidebar-link:hover {
      color: var(--color-lumyra-black);
      border-color: var(--color-lumyra-gray-400);
    }
    .sidebar-link.active {
      color: var(--color-lumyra-black);
      font-weight: 500;
      border-left: 2px solid var(--color-lumyra-black);
    }

    /* Content Area & Sections */
    .content-area {
      min-width: 0;
    }
    .section-wrap {
      padding-top: 3.5rem;
      padding-bottom: 3.5rem;
      border-bottom: 1px solid var(--color-lumyra-gray-200);
      scroll-margin-top: 5rem;
    }
    .section-wrap:last-child {
      border-bottom: none;
    }

    .section-header {
      margin-bottom: 2rem;
      max-width: 42rem;
    }
    .section-num {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--color-lumyra-gray-400);
    }
    .section-title {
      margin-top: 0.5rem;
      font-family: var(--font-display);
      font-size: 1.5rem;
      line-height: 1.25;
      font-weight: 500;
      letter-spacing: -0.025em;
      color: var(--color-lumyra-black);
    }
    @media (min-width: 640px) { .section-title { font-size: 1.875rem; } }
    .section-desc {
      margin-top: 0.5rem;
      font-size: 0.875rem;
      line-height: 1.625;
      color: var(--color-lumyra-gray-600);
    }

    /* Component Panel */
    .panel {
      border-radius: 0.5rem;
      border: 1px solid var(--color-lumyra-gray-200);
      background-color: var(--color-lumyra-white);
      margin-bottom: 1rem;
      overflow: hidden;
    }
    .panel-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      border-bottom: 1px solid var(--color-lumyra-gray-200);
      padding: 0.75rem 1.25rem;
    }
    .panel-title {
      font-size: 0.875rem;
      font-weight: 500;
      color: var(--color-lumyra-black);
    }
    .panel-body {
      padding: 1.25rem;
    }
    @media (min-width: 640px) { .panel-body { padding: 1.5rem; } }

    /* Button styles */
    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 0.375rem;
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      border: 1px solid transparent;
      transition: background-color 0.15s, color 0.15s;
    }
    .btn-primary { background-color: var(--color-lumyra-accent); color: #fff; }
    .btn-primary:hover { background-color: var(--color-lumyra-accent-hover); }
    .btn-dark { background-color: var(--color-lumyra-black); color: var(--color-lumyra-white); }
    .btn-dark:hover { background-color: var(--color-lumyra-gray-800); }
    .btn-secondary { background-color: var(--color-lumyra-white); border-color: var(--color-lumyra-gray-200); color: var(--color-lumyra-black); }
    .btn-secondary:hover { background-color: var(--color-lumyra-gray-100); }
    .btn-ghost { background-color: transparent; color: var(--color-lumyra-gray-600); }
    .btn-ghost:hover { background-color: var(--color-lumyra-gray-100); color: var(--color-lumyra-black); }
    .btn-danger { background-color: var(--color-lumyra-danger); color: #fff; }
    .btn-danger:hover { background-color: #dc2626; }
    .btn-disabled { background-color: var(--color-lumyra-gray-100); color: var(--color-lumyra-gray-400); cursor: not-allowed; }

    /* Toast */
    #toast {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      background-color: var(--color-lumyra-black);
      color: #fff;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      padding: 0.5rem 1rem;
      border-radius: var(--radius-button);
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s;
      z-index: 100;
    }
    #toast.show { opacity: 1; }
  </style>
</head>
<body>
  <div class="container">
    <!-- EXACT HERO HEADER -->
    <header class="hero">
      <div class="kicker-row">
        <p class="kicker">Getlumyra · Design System</p>
        <span class="dev-badge">
          <span class="dev-dot"></span>
          dev-only
        </span>
      </div>
      <h1 class="hero-title">Quiet surfaces, clear intent.</h1>
      <p class="hero-desc">
        Living specimen sheet and interactive explorer for Lumyra tokens. All values are single-sourced from
        <code class="inline-code">src/lib/design-tokens.ts</code>
        and compiled directly into Tailwind v4 <code class="inline-code">@theme</code>.
      </p>

      <dl class="stats-grid">
        <div class="stat-box">
          <dt class="stat-label">COLORS</dt>
          <dd class="stat-value tabular-nums">${stats[0].value}</dd>
        </div>
        <div class="stat-box">
          <dt class="stat-label">TYPE STYLES</dt>
          <dd class="stat-value tabular-nums">${stats[1].value}</dd>
        </div>
        <div class="stat-box">
          <dt class="stat-label">SPACING STEPS</dt>
          <dd class="stat-value tabular-nums">${stats[2].value}</dd>
        </div>
        <div class="stat-box">
          <dt class="stat-label">RADII</dt>
          <dd class="stat-value tabular-nums">${stats[3].value}</dd>
        </div>
      </dl>
    </header>

    <!-- EXACT 2-COLUMN EXPLORER LAYOUT -->
    <div class="explorer-layout">
      <div class="explorer-grid">
        <!-- Desktop Sticky Sidebar -->
        <aside class="sidebar">
          <div class="sidebar-sticky">
            <div class="search-wrap">
              <label for="ds-search" class="sr-only">Search tokens</label>
              <svg aria-hidden="true" viewBox="0 0 16 16" class="search-icon" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="7" cy="7" r="4.5" />
                <path d="m10.5 10.5 3 3" stroke-linecap="round" />
              </svg>
              <input
                id="ds-search"
                type="search"
                placeholder="Search tokens"
                oninput="filterTokens(this.value)"
                class="search-input"
              />
            </div>
            <nav aria-label="Sections">
              <ul class="sidebar-nav">
                <li><a href="#principles" class="sidebar-link active" data-nav="principles">Principles</a></li>
                <li><a href="#colors" class="sidebar-link" data-nav="colors">Color</a></li>
                <li><a href="#typography" class="sidebar-link" data-nav="typography">Typography</a></li>
                <li><a href="#spacing" class="sidebar-link" data-nav="spacing">Spacing</a></li>
                <li><a href="#radii" class="sidebar-link" data-nav="radii">Radius</a></li>
                <li><a href="#components" class="sidebar-link" data-nav="components">Components</a></li>
                <li><a href="#theme" class="sidebar-link" data-nav="theme">Theme code</a></li>
              </ul>
            </nav>
          </div>
        </aside>

        <!-- Main Content Stream (Divided sections 01-07) -->
        <div class="content-area">
          <!-- 01 Principles -->
          <section id="principles" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">01</p>
              <h2 class="section-title">Principles</h2>
              <p class="section-desc">Restraint over decoration. Every surface, border, and color carries a single, clear job.</p>
            </header>
            <ol class="grid gap-px overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-gray-200 sm:grid-cols-2" style="display: grid; gap: 1px; background-color: var(--color-lumyra-gray-200); border: 1px solid var(--color-lumyra-gray-200); border-radius: 0.5rem; list-style: none;">
              ${principlesHtml}
            </ol>
          </section>

          <!-- 02 Color -->
          <section id="colors" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">02</p>
              <h2 class="section-title">Color</h2>
              <p class="section-desc">Fourteen tokens across four roles. Click a swatch to copy its hex, or a chip to copy the variable or utility.</p>
            </header>
            <div id="colors-container">
              ${colorsHtml}
            </div>
          </section>

          <!-- 03 Typography -->
          <section id="typography" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">03</p>
              <h2 class="section-title">Typography</h2>
              <p class="section-desc">Geist for display, Inter for interface and prose, Geist Mono for identifiers. Nothing heavier than 500.</p>
            </header>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1px; background-color: var(--color-lumyra-gray-200); border: 1px solid var(--color-lumyra-gray-200); border-radius: 0.5rem; overflow: hidden; margin-bottom: 2rem;">
              <div class="bg-lumyra-white p-6" style="padding: 1.5rem;">
                <div class="font-display text-5xl font-medium tracking-tight text-lumyra-black" style="font-size: 3rem; font-weight: 500;">Aa</div>
                <h3 class="mt-5 text-sm font-medium text-lumyra-black" style="margin-top: 1.25rem; font-size: 0.875rem;">Geist</h3>
                <p class="mt-1 text-xs text-lumyra-gray-600" style="font-size: 0.75rem; color: var(--color-lumyra-gray-600);">Headlines, card titles, hero statements</p>
              </div>
              <div class="bg-lumyra-white p-6" style="padding: 1.5rem;">
                <div class="font-sans text-5xl font-medium tracking-tight text-lumyra-black" style="font-size: 3rem; font-weight: 500;">Aa</div>
                <h3 class="mt-5 text-sm font-medium text-lumyra-black" style="margin-top: 1.25rem; font-size: 0.875rem;">Inter</h3>
                <p class="mt-1 text-xs text-lumyra-gray-600" style="font-size: 0.75rem; color: var(--color-lumyra-gray-600);">Buttons, inputs, navigation, body copy</p>
              </div>
              <div class="bg-lumyra-white p-6" style="padding: 1.5rem;">
                <div class="font-mono text-5xl font-medium tracking-tight text-lumyra-black" style="font-size: 3rem; font-weight: 500;">Aa</div>
                <h3 class="mt-5 text-sm font-medium text-lumyra-black" style="margin-top: 1.25rem; font-size: 0.875rem;">Geist Mono</h3>
                <p class="mt-1 text-xs text-lumyra-gray-600" style="font-size: 0.75rem; color: var(--color-lumyra-gray-600);">Invite codes, dimensions, hex values</p>
              </div>
            </div>

            <div style="margin-bottom: 1rem;">
              <input
                id="ds-sample"
                type="text"
                placeholder="Type to preview your own copy across the scale"
                oninput="updateTypographySample(this.value)"
                style="width: 100%; border-radius: 0.375rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-white); padding: 0.5rem 0.75rem; font-size: 0.875rem; color: var(--color-lumyra-black);"
              />
            </div>

            <div style="border: 1px solid var(--color-lumyra-gray-200); border-radius: 0.5rem; background-color: var(--color-lumyra-white); divide-y: 1px solid var(--color-lumyra-gray-200);">
              ${typographyHtml}
            </div>
          </section>

          <!-- 04 Spacing -->
          <section id="spacing" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">04</p>
              <h2 class="section-title">Spacing</h2>
              <p class="section-desc">A tight, small-step scale for controls and cards, opening up at 24 and 32 for layout rhythm.</p>
            </header>
            <div style="border: 1px solid var(--color-lumyra-gray-200); border-radius: 0.5rem; background-color: var(--color-lumyra-white); overflow: hidden;">
              ${spacingHtml}
            </div>
          </section>

          <!-- 05 Radius -->
          <section id="radii" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">05</p>
              <h2 class="section-title">Radius</h2>
              <p class="section-desc">Corners stop at 8px. Pills and bubbly shapes are out; square edges handle structural lines.</p>
            </header>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem;">
              ${radiusHtml}
            </div>
            <div style="margin-top: 1rem; display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem;">
              <div style="border-radius: 0.5rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-white); padding: 1.25rem;">
                <p style="margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 500; color: var(--color-lumyra-success);">Do · 4–8px</p>
                <span style="display: inline-flex; height: 2.25rem; align-items: center; border-radius: 0.375rem; background-color: var(--color-lumyra-black); padding: 0 1rem; font-size: 0.875rem; font-weight: 500; color: #fff;">
                  Claim image
                </span>
              </div>
              <div style="border-radius: 0.5rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-white); padding: 1.25rem;">
                <p style="margin-bottom: 0.75rem; font-size: 0.75rem; font-weight: 500; color: var(--color-lumyra-danger);">Don’t · fully rounded</p>
                <span style="display: inline-flex; height: 2.25rem; align-items: center; border-radius: 9999px; background-color: var(--color-lumyra-gray-200); padding: 0 1rem; font-size: 0.875rem; font-weight: 500; color: var(--color-lumyra-gray-600);">
                  Claim image
                </span>
              </div>
            </div>
          </section>

          <!-- 06 Components -->
          <section id="components" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">06</p>
              <h2 class="section-title">Components</h2>
              <p class="section-desc">Live specimens built from the same utilities the product uses.</p>
            </header>
            <div style="display: flex; flex-direction: column; gap: 1rem;">
              <div class="panel">
                <div class="panel-header"><h3 class="panel-title">Buttons</h3></div>
                <div class="panel-body">
                  <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem;">
                    <button type="button" class="btn btn-primary">Primary</button>
                    <button type="button" class="btn btn-dark">Dark</button>
                    <button type="button" class="btn btn-secondary">Secondary</button>
                    <button type="button" class="btn btn-ghost">Ghost</button>
                    <button type="button" class="btn btn-danger">Destructive</button>
                    <button type="button" disabled class="btn btn-disabled">Disabled</button>
                  </div>
                </div>
              </div>

              <div class="panel">
                <div class="panel-header"><h3 class="panel-title">Badges</h3></div>
                <div class="panel-body">
                  <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 0.75rem;">
                    <span style="display: inline-flex; align-items: center; gap: 0.375rem; border-radius: 0.25rem; border: 1px solid #a7f3d0; background-color: #ecfdf5; padding: 0.125rem 0.625rem; font-size: 0.75rem; font-weight: 500; color: #065f46;">
                      <span style="width: 0.375rem; height: 0.375rem; border-radius: 9999px; background-color: var(--color-lumyra-success);"></span>
                      Available
                    </span>
                    <span style="display: inline-flex; align-items: center; gap: 0.375rem; border-radius: 0.25rem; border: 1px solid #ddd6fe; background-color: #f5f3ff; padding: 0.125rem 0.625rem; font-size: 0.75rem; font-weight: 500; color: #5b21b6;">
                      <span style="width: 0.375rem; height: 0.375rem; border-radius: 9999px; background-color: var(--color-lumyra-claimed);"></span>
                      Claimed
                    </span>
                    <span style="border-radius: 0.25rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-gray-100); padding: 0.125rem 0.5rem; font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-lumyra-gray-600);">
                      Beta
                    </span>
                    <span style="border-radius: 0.25rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-cream); padding: 0.125rem 0.625rem; font-family: var(--font-mono); font-size: 0.75rem; font-variant-numeric: tabular-nums; color: var(--color-lumyra-gray-800);">
                      LMYR-2026
                    </span>
                  </div>
                </div>
              </div>

              <div class="panel">
                <div class="panel-header"><h3 class="panel-title">Inputs</h3></div>
                <div class="panel-body">
                  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem;">
                    <div>
                      <label style="display: block; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.375rem; color: var(--color-lumyra-gray-800);">Title</label>
                      <input type="text" placeholder="Artwork title" style="width: 100%; border-radius: 0.375rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-white); padding: 0.5rem 0.75rem; font-size: 0.875rem;" />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.375rem; color: var(--color-lumyra-gray-800);">Invite code</label>
                      <input type="text" value="LMYR-2026-BETA" readonly style="width: 100%; border-radius: 0.375rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-cream); padding: 0.5rem 0.75rem; font-family: var(--font-mono); font-size: 0.875rem; letter-spacing: 0.1em; font-variant-numeric: tabular-nums;" />
                    </div>
                    <div>
                      <label style="display: block; font-size: 0.75rem; font-weight: 500; margin-bottom: 0.375rem; color: var(--color-lumyra-gray-800);">Email</label>
                      <input type="text" value="designer@" style="width: 100%; border-radius: 0.375rem; border: 1px solid var(--color-lumyra-danger); background-color: var(--color-lumyra-white); padding: 0.5rem 0.75rem; font-size: 0.875rem;" />
                      <p style="margin-top: 0.375rem; font-size: 0.75rem; color: var(--color-lumyra-danger);">Enter a valid email address.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 07 Theme code -->
          <section id="theme" class="section-wrap">
            <header class="section-header">
              <p class="section-num tabular-nums">07</p>
              <h2 class="section-title">Theme code</h2>
              <p class="section-desc">Tailwind v4 @theme block generated directly from tokens.</p>
            </header>
            <div style="position: relative;">
              <pre style="border-radius: 0.5rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-white); padding: 1.25rem; font-family: var(--font-mono); font-size: 0.75rem; line-height: 1.7; overflow-x: auto; color: var(--color-lumyra-black);"><code>${THEME_CSS}</code></pre>
              <button
                type="button"
                onclick="copyText(document.querySelector('#theme code').textContent)"
                style="position: absolute; top: 0.75rem; right: 0.75rem; border-radius: 0.375rem; border: 1px solid var(--color-lumyra-gray-200); background-color: var(--color-lumyra-white); padding: 0.25rem 0.5rem; font-family: var(--font-mono); font-size: 0.75rem; color: var(--color-lumyra-gray-600); cursor: pointer;"
              >
                Copy theme
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>

  <div id="toast">Copied to clipboard</div>

  <script>
    // Copy helper
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
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 1600);
    }

    // Typography live specimen
    function updateTypographySample(val) {
      document.querySelectorAll('.sample-render').forEach(el => {
        el.textContent = val || el.getAttribute('data-default');
      });
    }

    // Search filter across tokens
    function filterTokens(q) {
      q = q.toLowerCase().trim();
      document.querySelectorAll('[data-token-item]').forEach(el => {
        const text = el.getAttribute('data-token-item').toLowerCase();
        el.style.display = (!q || text.includes(q)) ? '' : 'none';
      });
    }

    // Active nav tracking on scroll
    const sections = ['principles', 'colors', 'typography', 'spacing', 'radii', 'components', 'theme'];
    window.addEventListener('scroll', () => {
      let current = sections[0];
      sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 140) current = id;
        }
      });
      document.querySelectorAll('.sidebar-link').forEach(link => {
        if (link.getAttribute('data-nav') === current) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    }, { passive: true });
  </script>
</body>
</html>
`;

writeFileSync(outPath, html, 'utf-8');
console.log('✓ Successfully generated identical interactive preview at', outPath);
