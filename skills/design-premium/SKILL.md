---
name: design-premium
description: Premium design system blueprint (Apple-style) — Inter typography, clean modern aesthetic, 4pt spacing scale. Strict K3 implementation guide for polished SaaS Next.js 15 apps.
---

# Premium Design System (K3 Blueprint)

> **Architect**: K3 Ecosystem (`bergside` inspired)
> **Target**: Next.js 15 + Tailwind v4 + Shadcn UI

## Mission
Execute frictionless, invisible UI that perfectly frames content. Soft borders, exquisite drop-shadows, mathematically perfect `Inter` kerning, and rounded precision.

## 1. Next.js Font Implantation
Inject these exact font definitions into `app/layout.tsx`:

```tsx
import { Inter, JetBrains_Mono } from 'next/font/google';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans', display: 'swap' });
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });

// Add to body className: `${inter.variable} ${jetbrainsMono.variable} font-sans antialiased bg-slate-50`
```

## 2. Tailwind v4 `@theme` Overrides (globals.css)
Inject these absolute value mappings to force Shadcn into the Premium paradigm.

```css
@theme inline {
  --color-background: #FFFFFF;
  --color-foreground: #09090B;
  
  --color-primary: #2563EB; /* Premium crisp blue */
  --color-primary-foreground: #FFFFFF;
  
  --color-secondary: #F4F4F5;
  --color-secondary-foreground: #09090B;
  
  --color-muted: #F4F4F5;
  --color-muted-foreground: #71717A;
  
  --color-accent: #F4F4F5;
  --color-accent-foreground: #09090B;
  
  --color-border: #E4E4E7;
  --color-input: #E4E4E7;
  --color-ring: #2563EB;
  
  --font-sans: var(--font-sans), ui-sans-serif, system-ui;
  --font-mono: var(--font-mono), ui-monospace, SFMono-Regular;
  
  --radius-xl: 1rem;
  --radius-lg: 0.75rem;
  --radius-md: calc(0.75rem - 2px);
  --radius-sm: calc(0.75rem - 4px);

  /* Signature Apple-style shadow elevation */
  --shadow-premium: 0 4px 24px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
}
```

## 3. UI Implementation Mandates
*   **Surfaces**: Favor cards sitting on a very light gray background (e.g., `body` bg `#FAFAFA`, card bg `#FFFFFF`), utilizing the custom `shadow-premium`.
*   **Corner Radii**: Aggressive rounding is required. Use `--radius-lg` and `--radius-xl` for structural containers and modals.
*   **Borders**: Almost entirely invisible (`border-[#E4E4E7]`) to create structure without visual noise.
*   **Text Weights**: Use `font-medium` (500) and `font-semibold` (600) strictly to map out hierarchy; never let text feel overly bold or "heavy" (avoid 800/900).
