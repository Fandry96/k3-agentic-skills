---
name: design-luxury
description: Luxury design system blueprint — dark surfaces, Oswald typography, bold expressive headings, 8pt grid. Strict K3 implementation guide for premium dark-mode Next.js 15 apps.
---

# Luxury Design System (K3 Blueprint)

> **Architect**: K3 Ecosystem (`bergside` inspired)
> **Target**: Next.js 15 + Tailwind v4 + Shadcn UI

## Mission
Execute a high-end, dramatic, expensive-feeling dark UI. Implement strict high-contrast text on true `#000000` backgrounds.

## 1. Next.js Font Implantation
Inject these exact font definitions into `app/layout.tsx`:

```tsx
import { Oswald, Inter, JetBrains_Mono } from 'next/font/google';

const oswald = Oswald({ subsets: ['latin'], variable: '--font-heading' });
const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });

// Add to body className: `${oswald.variable} ${inter.variable} ${jetbrainsMono.variable} font-sans antialiased`
```

## 2. Tailwind v4 `@theme` Overrides (globals.css)
Inject these absolute value mappings to force Shadcn into the Luxury paradigm.

```css
@theme inline {
  --color-background: #000000;
  --color-foreground: #FAFAFA;
  
  --color-primary: #FAFAFA;
  --color-primary-foreground: #000000;
  
  --color-secondary: #111111;
  --color-secondary-foreground: #E4E4E7;
  
  --color-muted: #111111;
  --color-muted-foreground: #A1A1AA;
  
  --color-accent: #222222;
  --color-accent-foreground: #FAFAFA;
  
  --color-border: #222222;
  --color-input: #222222;
  --color-ring: #FAFAFA;
  
  --font-sans: var(--font-sans), ui-sans-serif, system-ui;
  --font-heading: var(--font-heading), ui-sans-serif, system-ui;
  --font-mono: var(--font-mono), ui-monospace, SFMono-Regular;
  
  --radius-lg: 0px; /* Luxury favors sharp precision */
  --radius-md: 0px;
  --radius-sm: 0px;
}
```

## 3. UI Implementation Mandates
*   **Buttons**: Use sharp corners (radius 0). The primary action button must be solid white (`bg-primary text-primary-foreground`).
*   **Headings**: Must use the `font-heading` explicitly (e.g., `className="font-heading text-4xl uppercase tracking-widest"`).
*   **Whitespace**: Demand immense padding around structural elements.
*   **Borders**: Keep to an absolute minimum. Rely on spatial separation. If borders are used, they must be subtle (`border-border`, which maps to `#222222`).
