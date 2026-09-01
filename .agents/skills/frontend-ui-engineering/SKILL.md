---
name: frontend-ui-engineering
description: Comprehensive workflow and guidelines for building production-grade frontend applications, design systems, modern component libraries, and interactive UI/UX features with robust state handling.
---

# Frontend & UI/UX Engineering Workflow

This skill guides the design, architecture, and implementation of high-quality frontend interfaces, design systems, and responsive user experiences.

## 1. Design System Setup Workflow

When starting a project or building a new UI component suite:

### Step 1: Define Design Tokens (CSS Variables)
Establish standard tokens for colors, typography, shadows, radiuses, and transitions in `:root` and `[data-theme="dark"]`:

```css
:root {
  /* Color Palette - HSL / OKLCH */
  --bg-primary: hsl(0, 0%, 100%);
  --bg-secondary: hsl(210, 40%, 98%);
  --bg-surface: hsl(210, 40%, 96%);
  --text-primary: hsl(222, 47%, 11%);
  --text-secondary: hsl(215, 16%, 47%);
  --text-muted: hsl(215, 16%, 65%);
  --border-subtle: hsl(214, 32%, 91%);
  --accent: hsl(221, 83%, 53%);
  --accent-hover: hsl(221, 83%, 45%);
  --accent-foreground: hsl(0, 0%, 100%);
  
  /* Status Colors */
  --success: hsl(142, 76%, 36%);
  --warning: hsl(38, 92%, 50%);
  --danger: hsl(0, 84%, 60%);

  /* Typography */
  --font-sans: "Plus Jakarta Sans", "Inter", -apple-system, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Elevation & Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);

  /* Border Radii */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-full: 9999px;

  /* Animation Timings */
  --transition-fast: 150ms cubic-bezier(0.16, 1, 0.3, 1);
  --transition-normal: 250ms cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="dark"] {
  --bg-primary: hsl(224, 71%, 4%);
  --bg-secondary: hsl(222, 47%, 8%);
  --bg-surface: hsl(217, 33%, 12%);
  --text-primary: hsl(210, 40%, 98%);
  --text-secondary: hsl(215, 20%, 65%);
  --text-muted: hsl(215, 20%, 45%);
  --border-subtle: hsl(217, 33%, 18%);
  --accent: hsl(217, 91%, 60%);
  --accent-hover: hsl(217, 91%, 68%);
}
```

---

## 2. The 5-State Component Checklist

Every interactive component and page MUST account for all 5 states:

1. **Default / Success State**: The ideal rendering when data is present and valid.
2. **Loading State**: Skeleton loaders (with subtle shimmer) or loading spinners on action buttons with `aria-busy="true"`.
3. **Empty State**: Clear illustration/SVG icon, helpful headline, and a direct Call-To-Action (CTA) button to create the first item.
4. **Error State**: Friendly error message, retry button, contextual inline field errors with distinct icons and red tint.
5. **Partial / Stale State**: Graceful fallback when optional fields are null or network connection is slow.

---

## 3. Interaction & Animation Patterns

### Button States:
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 40px;
  padding: 0 16px;
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  user-select: none;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
  filter: brightness(1.05);
}

.btn:active:not(:disabled) {
  transform: translateY(0px) scale(0.98);
}

.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Card Elevation & Glassmorphism:
```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
}

.card-interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--accent);
}
```

---

## 4. UI/UX Pre-Delivery Quality Checklist

Before finalizing any frontend task, verify:
- [ ] **Contrast**: All text meets WCAG 2.1 AA (4.5:1 for body, 3:1 for large text).
- [ ] **Icons**: All icons are clean SVGs (no emoji icons).
- [ ] **Interactive Elements**: All interactive controls have visible hover, active, and `:focus-visible` styles.
- [ ] **Touch Targets**: Minimum 44x44px bounding box for touch devices.
- [ ] **Responsiveness**: Tested on Mobile (375px), Tablet (768px), and Desktop (1280px) with NO horizontal overflow.
- [ ] **Form Labels**: All form inputs have visible `<label>` tags with matching `for` / `id`.
- [ ] **Animations**: All transitions are smooth (150-300ms) and respect `prefers-reduced-motion`.
