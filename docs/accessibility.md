# Accessibility (a11y) & WCAG Compliance Checklist

This document details the accessibility standards and features implemented across the **ABTalks AI Interview Agent** UI.

---

## ♿ WCAG Checklist & Implementation

### 1. Keyboard Navigation & Focus Management
- Interactive elements (`Button`, links, inputs) have visible focus indicators via `focus-visible:ring-2 focus-visible:ring-emerald-400`.
- All forms and buttons are keyboard accessible via `<tab>` and `<enter>`.

### 2. ARIA Roles & Attributes
- Screen reader labels (`aria-label`, `aria-disabled`) added to form inputs and button components.
- Status announcements use `aria-live="polite"` or `role="alert"` for notification toasts and loading spinners.

### 3. Motion & Animation
- `motion-reduce:transition-none` applied to interactive components for users with reduced motion preferences (`prefers-reduced-motion`).

### 4. Color Contrast & Visuals
- High contrast color palette (slate-950 background with emerald-400 / slate-100 text) meeting WCAG AA standards.
