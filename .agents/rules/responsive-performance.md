---
description: Responsive layout, Core Web Vitals, and frontend performance rules
globs: ["**/*.{html,css,js,ts,jsx,tsx,vue,svelte}"]
---

# Responsive Layout & Frontend Performance

## 1. Responsive Layout Strategy
- **Mobile-First Paradigm**: Design the default CSS for mobile viewport, applying `min-width` media queries for larger screens.
- **Breakpoints**:
  - `sm`: 640px (Large phones / landscape)
  - `md`: 768px (Tablets)
  - `lg`: 1024px (Laptops / Small desktops)
  - `xl`: 1280px (Standard desktops)
  - `2xl`: 1536px (Ultra-wide displays)
- **Fluid Sizing**: Use `clamp()` for responsive typography and spacing:
  ```css
  font-size: clamp(1.5rem, 1rem + 2vw, 2.5rem);
  padding: clamp(1rem, 0.5rem + 1.5vw, 2.5rem);
  ```
- **Zero Horizontal Overflow**: Ensure `max-width: 100%`, `box-sizing: border-box`, and proper `word-break: break-word` on text containers.

## 2. Core Web Vitals (CWV)
- **Largest Contentful Paint (LCP < 2.5s)**:
  - Preload hero images using `<link rel="preload" as="image" href="...">` or `fetchpriority="high"`.
  - Avoid render-blocking synchronous scripts in `<head>`.
- **Cumulative Layout Shift (CLS < 0.1)**:
  - Always set explicit `width` and `height` or `aspect-ratio` on `<img>`, `<video>`, and `<iframe>`.
  - Reserve space for dynamic banners, ads, and asynchronously loaded elements.
- **Interaction to Next Paint (INP < 200ms)**:
  - Keep JavaScript event handlers lightweight; defer heavy calculations using `requestAnimationFrame`, `requestIdleCallback`, or Web Workers.
  - Optimize UI re-renders with component memoization and virtualization for lists > 100 items.

## 3. Modern CSS Techniques
- **Subgrid & Flex Gap**: Leverage `gap` property in Flexbox and CSS Grid.
- **Container Queries**: Use `@container (min-width: 400px)` for component-level responsiveness.
- **Logical Properties**: Prefer `margin-inline`, `padding-block`, `inset-inline-start` for seamless RTL support.
- **Color Palettes**: Leverage `color-mix()` and modern color spaces (`oklch()`, `hsl()`) for smooth color variants.
