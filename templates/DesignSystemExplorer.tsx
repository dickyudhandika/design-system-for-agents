// frontend/src/components/design-system/DesignSystemExplorer.tsx
import { useEffect, useMemo, useState } from 'preact/hooks';
import type { ComponentChildren } from 'preact';
import {
  COLOR_TOKENS,
  TYPOGRAPHY_TOKENS,
  SPACING_TOKENS,
  RADIUS_TOKENS,
  PRINCIPLES,
  type ColorToken,
} from '../../lib/design-tokens';

const SECTIONS = [
  { id: 'principles', label: 'Principles' },
  { id: 'colors', label: 'Color' },
  { id: 'typography', label: 'Typography' },
  { id: 'spacing', label: 'Spacing' },
  { id: 'radii', label: 'Radius' },
  { id: 'components', label: 'Components' },
  { id: 'theme', label: 'Theme code' },
] as const;

const SECTION_IDS = SECTIONS.map((s) => s.id);

const COLOR_GROUPS: { id: ColorToken['category']; label: string }[] = [
  { id: 'surfaces', label: 'Surfaces' },
  { id: 'neutrals', label: 'Neutrals' },
  { id: 'brand', label: 'Brand' },
  { id: 'states', label: 'States' },
];

// Radius token values are descriptive strings, so map ids to the rendered px.
const RADIUS_PX: Record<string, number> = { 'radius-card': 8, 'radius-button': 8, 'radius-none': 0 };

// Generated from the token list so the snippet can't drift from the swatches.
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

// Relative luminance check so swatch labels stay legible on any fill.
function isDarkHex(hex: string) {
  const n = parseInt(hex.slice(1), 16);
  const [r, g, b] = [(n >> 16) & 255, (n >> 8) & 255, n & 255].map((v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b < 0.4;
}

function useActiveSection(ids: readonly string[]) {
  const [active, setActive] = useState(ids[0]);
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting);
        if (visible.length) setActive(visible[0].target.id);
      },
      { rootMargin: '-120px 0px -65% 0px' }
    );
    ids.forEach((id) => {
      const el = document.getElementById(id);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, [ids]);
  return active;
}

function useCopy() {
  const [copied, setCopied] = useState<string | null>(null);
  useEffect(() => {
    if (!copied) return;
    const t = setTimeout(() => setCopied(null), 1600);
    return () => clearTimeout(t);
  }, [copied]);
  const copy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      // Clipboard can be blocked (insecure origin); still show feedback.
    }
    setCopied(text);
  };
  return { copied, copy };
}

function SectionHeader({ index, title, children }: { index: number; title: string; children?: ComponentChildren }) {
  return (
    <header class="mb-8 max-w-2xl">
      <p class="font-mono text-xs tabular-nums text-lumyra-gray-400">{String(index).padStart(2, '0')}</p>
      <h2 class="mt-2 font-display text-2xl sm:text-3xl font-medium tracking-tight text-balance text-lumyra-black">{title}</h2>
      {children && <p class="mt-2 text-sm leading-relaxed text-pretty text-lumyra-gray-600">{children}</p>}
    </header>
  );
}

function Panel({ title, action, children }: { title: string; action?: ComponentChildren; children: ComponentChildren }) {
  return (
    <div class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
      <div class="flex items-center justify-between gap-4 border-b border-lumyra-gray-200 px-5 py-3">
        <h3 class="text-sm font-medium text-lumyra-black">{title}</h3>
        {action}
      </div>
      <div class="p-5 sm:p-6">{children}</div>
    </div>
  );
}

function Empty({ query }: { query: string }) {
  return (
    <p class="rounded-lg border border-dashed border-lumyra-gray-200 px-5 py-8 text-center text-sm text-lumyra-gray-600">
      Nothing matches “{query}”.
    </p>
  );
}

function SearchField({ value, onChange, id }: { value: string; onChange: (v: string) => void; id: string }) {
  return (
    <div class="relative">
      <label for={id} class="sr-only">Search tokens</label>
      <svg aria-hidden="true" viewBox="0 0 16 16" class="pointer-events-none absolute left-3 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-lumyra-gray-400" fill="none" stroke="currentColor" stroke-width="1.5">
        <circle cx="7" cy="7" r="4.5" />
        <path d="m10.5 10.5 3 3" stroke-linecap="round" />
      </svg>
      <input
        id={id}
        type="search"
        value={value}
        onInput={(e) => onChange((e.target as HTMLInputElement).value)}
        placeholder="Search tokens"
        class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-white py-2 pl-9 pr-3 text-base sm:text-sm text-lumyra-black placeholder:text-lumyra-gray-400 focus:border-lumyra-accent focus:outline-none focus:ring-1 focus:ring-lumyra-accent"
      />
    </div>
  );
}

function CopyChip({ text, onCopy, copied }: { text: string; onCopy: (t: string) => void; copied: boolean }) {
  return (
    <button
      type="button"
      onClick={() => onCopy(text)}
      class="flex w-full items-center justify-between gap-2 rounded px-2 py-1 font-mono text-xs text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-lumyra-accent"
      aria-label={`Copy ${text}`}
    >
      <span class="truncate">{text}</span>
      <span class="shrink-0 text-[11px] text-lumyra-gray-400">{copied ? 'Copied' : 'Copy'}</span>
    </button>
  );
}

function ColorSwatch({ color, copy, copied }: { color: ColorToken; copy: (t: string) => void; copied: string | null }) {
  const dark = isDarkHex(color.hex);
  return (
    <div class="flex flex-col overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
      <button
        type="button"
        onClick={() => copy(color.hex)}
        style={{ backgroundColor: color.hex }}
        class={`group flex h-28 items-end justify-between border-b border-lumyra-gray-200 p-3 text-left font-mono text-xs cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-lumyra-accent ${
          dark ? 'text-lumyra-white' : 'text-lumyra-black'
        }`}
        aria-label={`Copy ${color.name} ${color.hex}`}
      >
        <span class="tabular-nums">{color.hex}</span>
        <span class="opacity-0 transition-opacity group-hover:opacity-70 group-focus-visible:opacity-70">
          {copied === color.hex ? 'Copied' : 'Copy'}
        </span>
      </button>
      <div class="flex flex-1 flex-col p-3">
        <p class="text-sm font-medium text-lumyra-black">{color.name}</p>
        <p class="mt-1 mb-3 flex-1 text-xs leading-relaxed text-pretty text-lumyra-gray-600">{color.role}</p>
        {color.wcag && <p class="mb-2 text-xs text-lumyra-gray-600">{color.wcag}</p>}
        <div class="-mx-2 space-y-0.5">
          <CopyChip text={`var(${color.cssVar})`} onCopy={copy} copied={copied === `var(${color.cssVar})`} />
          <CopyChip text={color.tailwindBg} onCopy={copy} copied={copied === color.tailwindBg} />
        </div>
      </div>
    </div>
  );
}

export function DesignSystemExplorer() {
  const [query, setQuery] = useState('');
  const [sampleText, setSampleText] = useState('');
  const [demoClaimed, setDemoClaimed] = useState(false);
  const active = useActiveSection(SECTION_IDS);
  const { copied, copy } = useCopy();

  const q = query.toLowerCase().trim();
  const matches = (...fields: string[]) => !q || fields.some((f) => f.toLowerCase().includes(q));

  const colorGroups = useMemo(
    () =>
      COLOR_GROUPS.map((g) => ({
        ...g,
        colors: COLOR_TOKENS.filter(
          (c) => c.category === g.id && matches(c.name, c.hex, c.cssVar, c.tailwindBg, c.role)
        ),
      })).filter((g) => g.colors.length),
    [q]
  );
  const types = useMemo(
    () => TYPOGRAPHY_TOKENS.filter((t) => matches(t.id, t.name, t.family, t.description)),
    [q]
  );
  const spacing = useMemo(
    () => SPACING_TOKENS.filter((s) => matches(s.token, s.usage, `${s.px}px`)),
    [q]
  );

  return (
    <div class="pb-24">
      {/* Mobile: sticky search + horizontal section nav */}
      <div class="sticky top-16 z-30 -mx-4 space-y-2 border-b border-lumyra-gray-200 bg-lumyra-white/95 px-4 py-3 backdrop-blur-md sm:-mx-6 sm:px-6 lg:hidden">
        <SearchField id="ds-search-mobile" value={query} onChange={setQuery} />
        <nav aria-label="Sections" class="-mx-1 flex gap-1 overflow-x-auto">
          {SECTIONS.map((s) => (
            <a
              key={s.id}
              href={`#${s.id}`}
              class={`whitespace-nowrap rounded-md px-2.5 py-1 text-xs font-medium transition-colors ${
                active === s.id ? 'bg-lumyra-black text-lumyra-white' : 'text-lumyra-gray-600 hover:text-lumyra-black'
              }`}
            >
              {s.label}
            </a>
          ))}
        </nav>
      </div>

      <div class="lg:grid lg:grid-cols-[200px_minmax(0,1fr)] lg:gap-16">
        {/* Desktop: sticky sidebar */}
        <aside class="hidden lg:block">
          <div class="sticky top-24 space-y-6 pt-14">
            <SearchField id="ds-search" value={query} onChange={setQuery} />
            <nav aria-label="Sections">
              <ul class="space-y-0.5 border-l border-lumyra-gray-200">
                {SECTIONS.map((s) => (
                  <li key={s.id}>
                    <a
                      href={`#${s.id}`}
                      aria-current={active === s.id ? 'true' : undefined}
                      class={`-ml-px block border-l py-1.5 pl-4 text-sm transition-colors ${
                        active === s.id
                          ? 'border-lumyra-black font-medium text-lumyra-black'
                          : 'border-transparent text-lumyra-gray-600 hover:border-lumyra-gray-400 hover:text-lumyra-black'
                      }`}
                    >
                      {s.label}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </aside>

        <div class="min-w-0 divide-y divide-lumyra-gray-200 [&>section]:py-14 [&>section]:scroll-mt-36 lg:[&>section]:scroll-mt-20">
          <section id="principles">
            <SectionHeader index={1} title="Principles">
              Restraint over decoration. Every surface, border, and color carries a single, clear job.
            </SectionHeader>
            <ol class="grid gap-px overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-gray-200 sm:grid-cols-2">
              {PRINCIPLES.map((p, i) => (
                <li key={p.title} class="bg-lumyra-white p-6">
                  <span class="font-mono text-xs tabular-nums text-lumyra-gray-400">{String(i + 1).padStart(2, '0')}</span>
                  <h3 class="mt-3 font-display text-base font-medium text-balance text-lumyra-black">{p.title}</h3>
                  <p class="mt-1.5 text-sm leading-relaxed text-pretty text-lumyra-gray-600">{p.desc}</p>
                </li>
              ))}
            </ol>
          </section>

          <section id="colors">
            <SectionHeader index={2} title="Color">
              Fourteen tokens across four roles. Click a swatch to copy its hex, or a chip to copy the variable or utility.
            </SectionHeader>
            {colorGroups.length === 0 && <Empty query={query} />}
            <div class="space-y-10">
              {colorGroups.map((g) => (
                <div key={g.id}>
                  <h3 class="mb-3 text-xs font-medium uppercase tracking-[0.1em] text-lumyra-gray-600">{g.label}</h3>
                  <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
                    {g.colors.map((c) => (
                      <ColorSwatch key={c.id} color={c} copy={copy} copied={copied} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section id="typography">
            <SectionHeader index={3} title="Typography">
              Geist for display, Inter for interface and prose, Geist Mono for identifiers. Nothing heavier than 500.
            </SectionHeader>

            <div class="mb-8 grid gap-px overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-gray-200 md:grid-cols-3">
              {[
                { name: 'Geist', cls: 'font-display', use: 'Headlines, card titles, hero statements' },
                { name: 'Inter', cls: 'font-sans', use: 'Buttons, inputs, navigation, body copy' },
                { name: 'Geist Mono', cls: 'font-mono', use: 'Invite codes, dimensions, hex values' },
              ].map((f) => (
                <div key={f.name} class="bg-lumyra-white p-6">
                  <div class={`${f.cls} text-5xl font-medium tracking-tight text-lumyra-black`}>Aa</div>
                  <h3 class="mt-5 text-sm font-medium text-lumyra-black">{f.name}</h3>
                  <p class="mt-1 text-xs text-lumyra-gray-600">{f.use}</p>
                </div>
              ))}
            </div>

            <div class="mb-4">
              <label for="ds-sample" class="sr-only">Sample text</label>
              <input
                id="ds-sample"
                type="text"
                value={sampleText}
                onInput={(e) => setSampleText((e.target as HTMLInputElement).value)}
                placeholder="Type to preview your own copy across the scale"
                class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-white px-3 py-2 text-base sm:text-sm text-lumyra-black placeholder:text-lumyra-gray-400 focus:border-lumyra-accent focus:outline-none focus:ring-1 focus:ring-lumyra-accent"
              />
            </div>

            {types.length === 0 ? (
              <Empty query={query} />
            ) : (
              <div class="divide-y divide-lumyra-gray-200 rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                {types.map((t) => {
                  const isUppercase = t.id === 'label-xs' || t.id === 'eyebrow';
                  return (
                    <div key={t.id} class="grid gap-3 px-5 py-5 md:grid-cols-[180px_minmax(0,1fr)] md:items-baseline md:gap-8">
                      <div>
                        <button
                          type="button"
                          onClick={() => copy(t.id)}
                          class="font-mono text-xs text-lumyra-black hover:text-lumyra-accent cursor-pointer"
                          aria-label={`Copy token ${t.id}`}
                        >
                          {copied === t.id ? 'Copied' : t.id}
                        </button>
                        <p class="mt-1 font-mono text-xs tabular-nums text-lumyra-gray-400">
                          {t.family} · {t.sizePx}/{t.weight}
                        </p>
                      </div>
                      <p
                        class={`${t.familyClass} ${isUppercase ? 'uppercase' : ''} truncate text-lumyra-black`}
                        style={{
                          fontSize: `${t.sizePx}px`,
                          fontWeight: t.weight,
                          letterSpacing: t.letterSpacing,
                        }}
                        title={t.description}
                      >
                        {sampleText || t.sampleText}
                      </p>
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          <section id="spacing">
            <SectionHeader index={4} title="Spacing">
              A tight, small-step scale for controls and cards, opening up at 24 and 32 for layout rhythm.
            </SectionHeader>
            {spacing.length === 0 ? (
              <Empty query={query} />
            ) : (
              <div class="divide-y divide-lumyra-gray-200 rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                {spacing.map((s) => (
                  <button
                    key={s.id}
                    type="button"
                    onClick={() => copy(`${s.px}px`)}
                    class="group grid w-full grid-cols-[72px_64px_minmax(0,1fr)] items-center gap-4 px-5 py-3 text-left transition-colors hover:bg-lumyra-gray-100/60 cursor-pointer focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-inset focus-visible:ring-lumyra-accent sm:grid-cols-[72px_64px_120px_minmax(0,1fr)]"
                    aria-label={`Copy spacing ${s.token}, ${s.px}px`}
                  >
                    <span class="font-mono text-xs tabular-nums text-lumyra-black">{s.token}</span>
                    <span class="font-mono text-xs tabular-nums text-lumyra-gray-600">
                      {copied === `${s.px}px` ? 'Copied' : `${s.px}px`}
                    </span>
                    <span class="hidden sm:block">
                      <span
                        class="block h-3 rounded-[2px] bg-lumyra-accent/80 transition-colors group-hover:bg-lumyra-accent"
                        style={{ width: `${s.px * 3}px` }}
                      />
                    </span>
                    <span class="truncate text-xs text-lumyra-gray-600">{s.usage}</span>
                  </button>
                ))}
              </div>
            )}
          </section>

          <section id="radii">
            <SectionHeader index={5} title="Radius">
              Corners stop at 8px. Pills and bubbly shapes are out; square edges handle structural lines.
            </SectionHeader>
            <div class="grid gap-4 md:grid-cols-3">
              {RADIUS_TOKENS.map((r) => (
                <div key={r.id} class="rounded-lg border border-lumyra-gray-200 bg-lumyra-white p-5">
                  <div
                    class="h-20 border border-lumyra-gray-400 bg-lumyra-cream"
                    style={{ borderRadius: `${RADIUS_PX[r.id] ?? 8}px` }}
                  />
                  <div class="mt-4 flex items-baseline justify-between gap-2">
                    <h3 class="text-sm font-medium text-lumyra-black">{r.name}</h3>
                    <span class="font-mono text-xs tabular-nums text-lumyra-gray-600">{RADIUS_PX[r.id] ?? 8}px</span>
                  </div>
                  <p class="mt-1 text-xs leading-relaxed text-pretty text-lumyra-gray-600">{r.description}</p>
                </div>
              ))}
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
                {/* Inline radius: the theme caps rounded-* utilities at 8px. */}
                <span
                  class="inline-flex h-9 items-center bg-lumyra-gray-200 px-4 text-sm font-medium text-lumyra-gray-600"
                  style={{ borderRadius: '9999px' }}
                >
                  Claim image
                </span>
              </div>
            </div>
          </section>

          <section id="components">
            <SectionHeader index={6} title="Components">
              Live specimens built from the same utilities the product uses.
            </SectionHeader>
            <div class="space-y-4">
              <Panel title="Buttons">
                <div class="flex flex-wrap items-center gap-3">
                  <button type="button" class="rounded-md bg-lumyra-accent px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-lumyra-accent-hover cursor-pointer">
                    Primary
                  </button>
                  <button type="button" class="rounded-md bg-lumyra-black px-4 py-2 text-sm font-medium text-lumyra-white transition-colors hover:bg-lumyra-gray-800 cursor-pointer">
                    Dark
                  </button>
                  <button type="button" class="rounded-md border border-lumyra-gray-200 bg-lumyra-white px-4 py-2 text-sm font-medium text-lumyra-black transition-colors hover:bg-lumyra-gray-100 cursor-pointer">
                    Secondary
                  </button>
                  <button type="button" class="rounded-md px-4 py-2 text-sm font-medium text-lumyra-gray-600 transition-colors hover:bg-lumyra-gray-100 hover:text-lumyra-black cursor-pointer">
                    Ghost
                  </button>
                  <button type="button" class="rounded-md bg-lumyra-danger px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-red-600 cursor-pointer">
                    Destructive
                  </button>
                  <button type="button" disabled class="rounded-md bg-lumyra-gray-100 px-4 py-2 text-sm font-medium text-lumyra-gray-400 cursor-not-allowed">
                    Disabled
                  </button>
                </div>
              </Panel>

              <Panel title="Badges">
                <div class="flex flex-wrap items-center gap-3">
                  <span class="inline-flex items-center gap-1.5 rounded border border-emerald-200 bg-emerald-50 px-2.5 py-0.5 text-xs font-medium text-emerald-800">
                    <span class="h-1.5 w-1.5 rounded-full bg-lumyra-success" />
                    Available
                  </span>
                  <span class="inline-flex items-center gap-1.5 rounded border border-violet-200 bg-violet-50 px-2.5 py-0.5 text-xs font-medium text-violet-800">
                    <span class="h-1.5 w-1.5 rounded-full bg-lumyra-claimed" />
                    Claimed
                  </span>
                  <span class="rounded border border-lumyra-gray-200 bg-lumyra-gray-100 px-2 py-0.5 text-xs font-medium uppercase tracking-wider text-lumyra-gray-600">
                    Beta
                  </span>
                  <span class="rounded border border-lumyra-gray-200 bg-lumyra-cream px-2.5 py-0.5 font-mono text-xs tabular-nums text-lumyra-gray-800">
                    LMYR-2026
                  </span>
                </div>
              </Panel>

              <Panel title="Inputs">
                <div class="grid gap-5 md:grid-cols-3">
                  <div>
                    <label for="ds-in-default" class="mb-1.5 block text-xs font-medium text-lumyra-gray-800">Title</label>
                    <input id="ds-in-default" type="text" placeholder="Artwork title" class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-white px-3 py-2 text-base sm:text-sm text-lumyra-black placeholder:text-lumyra-gray-400 focus:border-lumyra-accent focus:outline-none focus:ring-1 focus:ring-lumyra-accent" />
                  </div>
                  <div>
                    <label for="ds-in-code" class="mb-1.5 block text-xs font-medium text-lumyra-gray-800">Invite code</label>
                    <input id="ds-in-code" type="text" value="LMYR-2026-BETA" readOnly class="w-full rounded-md border border-lumyra-gray-200 bg-lumyra-cream px-3 py-2 font-mono text-base sm:text-sm tracking-widest tabular-nums text-lumyra-black focus:outline-none" />
                  </div>
                  <div>
                    <label for="ds-in-error" class="mb-1.5 block text-xs font-medium text-lumyra-gray-800">Email</label>
                    <input id="ds-in-error" type="text" value="designer@" aria-invalid="true" aria-describedby="ds-in-error-msg" class="w-full rounded-md border border-lumyra-danger bg-lumyra-white px-3 py-2 text-base sm:text-sm text-lumyra-black focus:outline-none focus:ring-1 focus:ring-lumyra-danger" />
                    <p id="ds-in-error-msg" class="mt-1.5 text-xs text-lumyra-danger">Enter a valid email address.</p>
                  </div>
                </div>
              </Panel>

              <Panel
                title="Artwork card"
                action={
                  <div role="group" aria-label="Card state" class="flex rounded-md bg-lumyra-gray-100 p-0.5 text-xs font-medium">
                    {[false, true].map((claimed) => (
                      <button
                        key={String(claimed)}
                        type="button"
                        aria-pressed={demoClaimed === claimed}
                        onClick={() => setDemoClaimed(claimed)}
                        class={`rounded px-2.5 py-1 transition-colors cursor-pointer ${
                          demoClaimed === claimed ? 'bg-lumyra-white text-lumyra-black shadow-xs' : 'text-lumyra-gray-600 hover:text-lumyra-black'
                        }`}
                      >
                        {claimed ? 'Claimed' : 'Available'}
                      </button>
                    ))}
                  </div>
                }
              >
                <div class="mx-auto max-w-xs overflow-hidden rounded-lg border border-lumyra-gray-200 bg-lumyra-white">
                  <div class="relative flex aspect-4/3 items-center justify-center bg-lumyra-gray-100">
                    <span class="font-mono text-xs tabular-nums text-lumyra-gray-400">4:3</span>
                    <span
                      class={`absolute right-2.5 top-2.5 rounded px-2.5 py-0.5 text-xs font-medium text-white ${
                        demoClaimed ? 'bg-lumyra-claimed' : 'bg-lumyra-success'
                      }`}
                    >
                      {demoClaimed ? 'Claimed' : 'Available'}
                    </span>
                  </div>
                  <div class="p-4">
                    <div class="flex items-center justify-between text-xs text-lumyra-gray-600">
                      <span class="font-mono tabular-nums">#042</span>
                      <span>Abstract</span>
                    </div>
                    <p class="mt-1.5 font-display text-base font-medium text-lumyra-black">Prismatic Monolith No. 4</p>
                    <div class="mt-3 flex items-center justify-between border-t border-lumyra-gray-100 pt-3">
                      <span class="font-mono text-xs tabular-nums text-lumyra-gray-400">2464 × 1856</span>
                      <button
                        type="button"
                        disabled={demoClaimed}
                        class={`rounded-md px-3 py-1 text-xs font-medium transition-colors ${
                          demoClaimed
                            ? 'bg-lumyra-gray-100 text-lumyra-gray-400 cursor-not-allowed'
                            : 'bg-lumyra-black text-lumyra-white hover:bg-lumyra-gray-800 cursor-pointer'
                        }`}
                      >
                        {demoClaimed ? 'Locked' : 'Claim'}
                      </button>
                    </div>
                  </div>
                </div>
              </Panel>
            </div>
          </section>

          <section id="theme">
            <SectionHeader index={7} title="Theme code">
              The Tailwind v4 <code class="font-mono text-xs text-lumyra-black">@theme</code> block behind every token above.
            </SectionHeader>
            <div class="overflow-hidden rounded-lg border border-lumyra-gray-800 bg-lumyra-black">
              <div class="flex items-center justify-between border-b border-lumyra-gray-800 px-4 py-2.5">
                <span class="font-mono text-xs text-lumyra-gray-400">global.css</span>
                <button
                  type="button"
                  onClick={() => copy(THEME_CSS)}
                  class="rounded px-2 py-1 font-mono text-xs text-lumyra-gray-400 transition-colors hover:bg-lumyra-gray-800 hover:text-lumyra-white cursor-pointer"
                >
                  {copied === THEME_CSS ? 'Copied' : 'Copy'}
                </button>
              </div>
              <pre class="overflow-x-auto p-5 font-mono text-xs leading-relaxed text-lumyra-gray-200">{THEME_CSS}</pre>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
