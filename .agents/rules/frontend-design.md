---
description: Modern visual design, aesthetics, typography, color theory, and micro-interaction guidelines for frontend engineering
globs: ["**/*.{html,css,js,ts,jsx,tsx,vue,svelte}"]
---

# Modern Frontend & Visual Design Rules

## 1. Visual Hierarchy & Aesthetics
- **Depth & Dimension**: Use layered z-indexes with soft shadows (`box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05), 0 2px 6px -1px rgba(0, 0, 0, 0.03)`).
- **Glassmorphism**: When using frosted glass, pair `backdrop-filter: blur(12px)` with subtle 1px border (`border: 1px solid rgba(255, 255, 255, 0.1)` in dark mode or `rgba(0, 0, 0, 0.06)` in light mode).
- **Anti-AI Default**: Avoid saturated violet-to-cyan gradients. Choose intentional palettes:
  - Slate / Indigo / Amber (Modern SaaS)
  - Zinc / Emerald / Neutral (Clean Fintech / Developer Tools)
  - Warm Sand / Terracotta / Charcoal (Editorial & Lifestyle)

## 2. Typography Rules
- **Base Size**: 16px (1rem) for body text to ensure readability on all viewports.
- **Line Heights**:
  - Headings: `1.1 - 1.25`
  - Body copy: `1.5 - 1.65`
  - Compact UI / Badges: `1.0 - 1.2`
- **Font Pairing**:
  - Primary UI: Plus Jakarta Sans, Inter, Outfit, DM Sans
  - Monospace / Data / Code: JetBrains Mono, Fira Code
  - Editorial / Serif accents: Playfair Display, Instrument Serif
- **Hierarchy**: Maximum 3 font weights per page (Regular 400, Medium 500, Semibold/Bold 600/700).

## 3. Spacing & The 8px Grid
- Use the 8pt/4pt increment system: `4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px`.
- Consistent padding inside cards (`p-4` or `p-6`).
- Section separation: `py-12` (mobile) to `py-24` (desktop).

## 4. Micro-Interactions & Motion
- **Transitions**: All interactive state changes must transition (`transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1)`).
- **Button Feedback**:
  - Hover: subtle brightness / elevation increase (`transform: translateY(-1px)`).
  - Active: slight compression (`transform: translateY(0px) scale(0.98)`).
- **Skeleton Screens**: Prefer animated pulse skeletons over generic full-page spinners for content-heavy views.
- **Reduced Motion**: Always support `@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }`.

## 5. Anti-Patterns to Strictly Avoid
- NEVER use emoji characters for UI icons. Use SVG icon sets (Lucide, Heroicons, Phosphor).
- NEVER use 0ms instantaneous state changes for hover/focus.
- NEVER create unclickable small hit areas (buttons/links must be at least 44x44px bounding area).
- NEVER hide focus rings (`outline: none`) without providing an explicit replacement `:focus-visible` style.
- NEVER mix conflicting border-radii randomly (e.g. sharp 2px cards with circular 9999px inputs).
