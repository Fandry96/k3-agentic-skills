---
name: design-elegant
description: Elegant design system blueprint — Google Sans (Outfit), minimal aesthetic. Strict K3 implementation guide for refined, light-weight UI in Next.js 15.
---

# Elegant Design System (K3 Blueprint)

> **Architect**: K3 Ecosystem (`bergside` inspired)
> **Target**: Next.js 15 + Tailwind v4 + Shadcn UI

## Mission
Execute weightless, delicate interfaces. Emphasize incredible precision via extremely thin borders, subtle typography, and a deliberate absence of visual noise.

## 1. Next.js Font Implantation
Inject these exact font definitions into `app/layout.tsx`. (Note: Google Sans is proprietary and unlisted in `next/font`, so we substitute with the closest open match: purely geometric `Outfit` or `Plus Jakarta Sans`).

```tsx
import { Outfit, Anonymous_Pro } from 'next/font/google';

const outfit = Outfit({ subsets: ['latin'], variable: '--font-sans' });
const anonymousPro = Anonymous_Pro({ subsets: ['latin'], weight: ['400', '700'], variable: '--font-mono' });

// Add to body className: `${outfit.variable} ${anonymousPro.variable} font-sans antialiased text-gray-900`
```

## 2. Tailwind v4 `@theme` Overrides (globals.css)
Inject these absolute value mappings to force Shadcn into the Elegant paradigm.

```css
@theme inline {
  --color-background: #FCFCFD;
  --color-foreground: #09090B;
  
  --color-primary: #18181B; /* Almost black */
  --color-primary-foreground: #FAFAFA;
  
  --color-secondary: #FAFAFA;
  --color-secondary-foreground: #18181B;
  
  --color-muted: #F4F4F5;
  --color-muted-foreground: #71717A;
  
  --color-accent: #F4F4F5;
  --color-accent-foreground: #18181B;
  
  --color-border: #E4E4E7;
  --color-input: #E4E4E7;
  --color-ring: #18181B;
  
  --font-sans: var(--font-sans), ui-sans-serif, system-ui;
  --font-mono: var(--font-mono), ui-monospace, SFMono-Regular;
  
  --radius-lg: 0.375rem;
  --radius-md: calc(0.375rem - 2px);
  --radius-sm: calc(0.375rem - 4px);
}

@utility thin-border {
  border-width: 0.5px; /* Deliberately sub-pixel for elegance on high-DPI screens! */
  border-color: var(--color-border);
}
```

## 3. UI Implementation Mandates
*   **Typography Scale**: Favor extremely tight geometry. Do not use `font-bold` lightly; maximum weight should usually be `font-medium` or `font-semibold` unless making a massive stylistic statement.
*   **Sub-Pixel Borders**: The hallmark of elegant UI is thinness. Standard `1px` borders can feel heavy. Use the provided `@utility thin-border` on Cards and Inputs where high-DPI retina rendering is expected.
*   **Color Paradigm**: Rely exclusively on monochrome contrast (Black vs White vs #FAFAFA) for structural elements, reserving true accent hues (like `#3B82F6`) *only* for solitary, high-value primary CTAs.
