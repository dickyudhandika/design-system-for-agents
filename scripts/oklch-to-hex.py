#!/usr/bin/env python3
"""oklch → hex conversion for shadcn/ui theme vars.

Reads CSS custom properties (oklch or hex) from stdin or a file and prints
the same vars converted to hex. Used by ds4a detection of shadcn themes (references/shadcn-baseline.md).

Usage:
    cat globals.css | python3 oklch-to-hex.py
    python3 oklch-to-hex.py globals.css

Handles:
    --background: oklch(1 0 0);
    --primary: oklch(0.205 0 0);
    --border: oklch(1 0 0 / 10%);
    --radius: 0.625rem;              (left untouched — non-color)
    #FFFFFF;                          (already hex, passthrough)

Output preserves variable names + light/dark block structure.
"""

import re
import sys
from pathlib import Path


def oklch_to_srgb(L, C, H):
    """OKLCH → sRGB, values in [0,1]. Mirrors the CSS Color 4 reference algorithm."""
    import math

    # Convert OKLCH to OKLab
    if H is None:
        a = b = 0.0
    else:
        h = math.radians(H)
        a = C * math.cos(h)
        b = C * math.sin(h)

    # OKLab → linear sRGB
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3

    r_lin = +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g_lin = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b_lin = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s

    def to_gamma(x: float) -> float:
        x = max(0.0, min(1.0, x))
        if x <= 0.0031308:
            return 12.92 * x
        return 1.055 * (x ** (1 / 2.4)) - 0.055

    return to_gamma(r_lin), to_gamma(g_lin), to_gamma(b_lin)


def to_hex(vals):
    r, g, b = (round(max(0.0, min(1.0, v)) * 255) for v in vals)
    return f"#{r:02X}{g:02X}{b:02X}"


# --color: oklch(L C H / alpha)   or   oklch(L C H)
# alpha is a percentage or number; hex output drops alpha (approximation).
# For alpha < 1 we emit 8-digit hex so the tint survives.
oklch_re = re.compile(
    r"oklch\(\s*"
    r"([0-9.]+)\s+"          # L
    r"([0-9.]+)\s+"          # C
    r"([0-9.]+)\s*"          # H
    r"(?:\/\s*([0-9.]+%?)\s*)?"
    r"\)",
    re.IGNORECASE,
)


def convert_line(line: str) -> str:
    def repl(m: re.Match) -> str:
        L, C, H = float(m.group(1)), float(m.group(2)), float(m.group(3))
        alpha = m.group(4)
        hex6 = to_hex(oklch_to_srgb(L, C, H))
        if alpha is None:
            return hex6
        a = float(alpha.rstrip("%")) / 100 if alpha.endswith("%") else float(alpha)
        a_255 = round(max(0.0, min(1.0, a)) * 255)
        return f"{hex6}{a_255:02X}"
    return oklch_re.sub(repl, line)


def main() -> int:
    if len(sys.argv) > 1:
        text = Path(sys.argv[1]).read_text()
    else:
        text = sys.stdin.read()

    for line in text.splitlines(keepends=True):
        # Skip comments; keep them for context
        sys.stdout.write(convert_line(line))
    return 0


if __name__ == "__main__":
    sys.exit(main())
