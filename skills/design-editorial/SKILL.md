---
name: design-editorial
description: Editorial design system blueprint — Gelasio serif typography, modern editorial layouts, 8pt grid, WCAG 2.2 AA. Strict K3 implementation guide for magazine-style Next.js 15 apps.
---

# Editorial Design System (K3 Blueprint)

> **Architect**: K3 Ecosystem (`bergside` inspired)
> **Target**: Next.js 15 + Tailwind v4 + Shadcn UI

## Mission
Execute publication-grade readability. Prioritize serif headings, massive body text legibility, and high-fidelity contrast on soft backgrounds.

## 1. Next.js Font Implantation
Inject these exact font definitions into `app/layout.tsx`:

```tsx
import { Gelasio, Inter, Ubuntu_Mono } from 'next/font/google';

const gelasio = Gelasio({ subsets: ['latin'], weight: ['400', '500', '600', '700'], variable: '--font-serif' });
const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });
const ubuntuMono = Ubuntu_Mono({ subsets: ['latin'], weight: '400', variable: '--font-mono' });

// Add to body className: `${gelasio.variable} ${inter.variable} ${ubuntuMono.variable} font-sans antialiased text-pretty`
```

## 2. Tailwind v4 `@theme` Overrides (globals.css)
Inject these absolute value mappings to force Shadcn into the Editorial paradigm.

```css
@theme inline {
  --color-background: #FDFDFD;
  --color-foreground: #111111;
  
  --color-primary: #111111;
  --color-primary-foreground: #FFFFFF;
  
  --color-secondary: #F1F1F1;
  --color-secondary-foreground: #111111;
  
  --color-muted: #F1F1F1;
  --color-muted-foreground: #6B7280;
  
  --color-accent: #E5E5E5;
  --color-accent-foreground: #111111;
  
  --color-border: #E5E5E5;
  --color-input: #E5E5E5;
  --color-ring: #111111;
  
  --font-serif: var(--font-serif), ui-serif, Georgia, Cambria, 'Times New Roman', Times, serif;
  --font-sans: var(--font-sans), ui-sans-serif, system-ui;
  --font-mono: var(--font-mono), ui-monospace, SFMono-Regular;
  
  --radius-lg: 0.25rem;
  --radius-md: calc(0.25rem - 2px);
  --radius-sm: calc(0.25rem - 4px);
}
```

## 3. UI Implementation Mandates
*   **Typography Hierarchy**: All `h1`, `h2`, `h3` must explicitly invoke the serif stack (`font-serif tracking-tight`).
*   **Body Copy**: Use `text-lg` or `text-xl` for primary articles with a relaxed line-height (`leading-relaxed` or `leading-loose`).
*   **Separators**: Utilize literal `<hr>` components heavily styled with `border-muted` to simulate print columns and breaks.
*   **Images**: Require strict captions underneath, styled in `font-sans text-sm text-muted-foreground`.
