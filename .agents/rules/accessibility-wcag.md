---
description: Accessibility (a11y) and WCAG 2.1 AA standards for HTML/CSS/JS frontend components
globs: ["**/*.{html,css,js,ts,jsx,tsx,vue,svelte}"]
---

# Accessibility & WCAG 2.1 AA Guidelines

## 1. Color Contrast Requirements
- **Normal Text (< 18pt / 24px)**: Minimum contrast ratio of **4.5:1** against background.
- **Large Text (>= 18pt / 24px or 14pt bold)**: Minimum contrast ratio of **3:1**.
- **UI Components & Graphical Objects**: Minimum contrast ratio of **3:1** for borders, icons, and focus indicators.
- **Do not rely on color alone**: Errors, warnings, and states must have an accompanying text label, icon, or pattern.

## 2. Keyboard Navigation & Focus Management
- Every interactive element (button, link, input, modal trigger) must be reachable via `Tab` and operable via `Enter` or `Space`.
- **Visible Focus Indicator**:
  ```css
  :focus-visible {
    outline: 2px solid var(--focus-ring, #3b82f6);
    outline-offset: 2px;
  }
  ```
- **Modals & Dialogs**: Trap keyboard focus inside open modals; return focus to trigger on close; support `Escape` to dismiss.

## 3. Semantic Structure & ARIA
- Use semantic HTML tags: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`, `<article>`, `<section>`.
- Use a single `<h1>` per page, following hierarchical `<h2>` to `<h6>` without skipping levels.
- **Accessible Names**:
  - Icon buttons must have `aria-label="Action name"` or visually hidden text (`<span class="sr-only">Action</span>`).
  - Inputs must have an associated `<label for="id">` or `aria-labelledby`.
  - Dynamic status changes must use `aria-live="polite"` or `role="status"`.

## 4. Touch Targets & Responsive Inputs
- Minimum touch target size: **44px x 44px** (with padding if the visible icon is smaller).
- Spacing between adjacent touch targets: at least **8px**.
- Mobile form inputs must prevent automatic zoom on iOS by setting `font-size: 16px` (or 1rem).
