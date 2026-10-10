// frontend/scripts/build-tokens.ts
import { writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  COLOR_TOKENS,
  RADIUS_TOKENS,
} from '../src/lib/design-tokens.ts';

const __dirname = dirname(fileURLToPath(import.meta.url));
const outputPath = resolve(__dirname, '../src/styles/tokens.generated.css');

function generateCss(): string {
  const lines: string[] = [
    '/**',
    ' * AUTO-GENERATED DESIGN TOKENS — DO NOT EDIT DIRECTLY',
    ' * Source of truth: frontend/src/lib/design-tokens.ts',
    ' * Regenerate with: npm run build:tokens',
    ' */',
    '',
    '@theme {',
    '  /* Colors */',
  ];

  for (const token of COLOR_TOKENS) {
    lines.push(`  ${token.cssVar}: ${token.hex};`);
  }

  lines.push('');
  lines.push('  /* Typography */');
  lines.push("  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;");
  lines.push("  --font-display: 'Geist', system-ui, sans-serif;");
  lines.push("  --font-mono: 'Geist Mono', ui-monospace, monospace;");

  lines.push('');
  lines.push('  /* Container & Layout */');
  lines.push('  --container-max: 1280px;');

  lines.push('');
  lines.push('  /* Radius (Capped at 8px / 0.5rem per Lumyra architectural principle) */');
  lines.push('  --radius-card: 0.5rem;');
  lines.push('  --radius-button: 0.5rem;');
  lines.push('  --radius-lg: 0.5rem;');
  lines.push('  --radius-xl: 0.5rem;');
  lines.push('  --radius-2xl: 0.5rem;');
  lines.push('  --radius-3xl: 0.5rem;');
  lines.push('  --radius-4xl: 0.5rem;');
  lines.push('}');
  lines.push('');

  return lines.join('\n');
}

const css = generateCss();
writeFileSync(outputPath, css, 'utf-8');
console.log(`✓ Generated ${outputPath} (${COLOR_TOKENS.length} colors, fonts, layout, and capped radii)`);
