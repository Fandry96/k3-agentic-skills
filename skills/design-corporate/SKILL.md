---
name: design-corporate
description: Corporate design system blueprint — Open Sans/Poppins typography, enterprise layouts. Strict K3 implementation guide for B2B/Admin dashboards in Next.js 15.
---

# Corporate Design System (K3 Blueprint)

> **Architect**: K3 Ecosystem (`bergside` inspired)
> **Target**: Next.js 15 + Tailwind v4 + Shadcn UI

## Mission
Execute trustworthy, highly-dense, data-rich interfaces that command operational authority. High legibility, strict component alignment, and standardized corporate blue/gray scale.

## 1. Next.js Font Implantation
Inject these exact font definitions into `app/layout.tsx`:

```tsx
import { Open_Sans, Poppins, IBM_Plex_Mono } from 'next/font/google';

const poppins = Poppins({ subsets: ['latin'], weight: ['500', '600', '700'], variable: '--font-heading' });
const openSans = Open_Sans({ subsets: ['latin'], variable: '--font-sans' });
const plexMono = IBM_Plex_Mono({ subsets: ['latin'], weight: ['400', '500'], variable: '--font-mono' });

// Add to body className: `${poppins.variable} ${openSans.variable} ${plexMono.variable} font-sans antialiased text-slate-800`
```

## 2. Tailwind v4 `@theme` Overrides (globals.css)
Inject these absolute value mappings to force Shadcn into the Corporate paradigm.

```css
@theme inline {
  --color-background: #F8FAFC;
  --color-foreground: #0F172A;
  
  --color-primary: #1E40AF; /* Trustworthy Corporate Blue */
  --color-primary-foreground: #FFFFFF;
  
  --color-secondary: #E2E8F0;
  --color-secondary-foreground: #0F172A;
  
  --color-muted: #F1F5F9;
  --color-muted-foreground: #64748B;
  
  --color-accent: #E2E8F0;
  --color-accent-foreground: #0F172A;
  
  --color-border: #CBD5E1;
  --color-input: #CBD5E1;
  --color-ring: #1E40AF;
  
  --color-success: #16A34A;
  --color-warning: #D97706;
  --color-danger: #DC2626;
  
  --font-sans: var(--font-sans), ui-sans-serif, system-ui;
  --font-heading: var(--font-heading), ui-sans-serif, system-ui;
  --font-mono: var(--font-mono), ui-monospace, SFMono-Regular;
  
  --radius-lg: 0.5rem;
  --radius-md: calc(0.5rem - 2px);
  --radius-sm: calc(0.5rem - 4px);
}
```

## 3. UI Implementation Mandates
*   **Information Density**: B2B tools require density. Use standard `size="sm"` components for forms and tables to maximize screen real estate.
*   **Cards**: All content must be housed in `bg-white border border-border shadow-sm` containers. Floating components are not permitted.
*   **Action Verbs**: Primary buttons must exclusively be the corporate Blue (`bg-primary`); secondary/cancel workflows must exclusively be gray contours (`variant="outline"`).
*   **Data Grids**: Mandate the usage of `IBM Plex Mono` for all tabular financial, metric, and ID data within Data Tables.
