---
name: design-glassmorphism
description: Glassmorphism design system blueprint — frosted glass effects, backdrop-blur, liquid depth. Strict K3 implementation guide for complex UI layering in Next.js 15 apps.
---

# Glassmorphism Design System (K3 Blueprint)

> **Architect**: K3 Ecosystem (`bergside` inspired)
> **Target**: Next.js 15 + Tailwind v4 + Shadcn UI

## Mission
Execute translucent, multi-plane layering. Elements must appear to float over vibrant, dynamic backdrops using rigorous blur and structural transparency.

## 1. Next.js Font Implantation
Inject these exact font definitions into `app/layout.tsx`:

```tsx
import { Plus_Jakarta_Sans, JetBrains_Mono } from 'next/font/google';

const jakarta = Plus_Jakarta_Sans({ subsets: ['latin'], variable: '--font-sans' });
const jetbrainsMono = JetBrains_Mono({ subsets: ['latin'], variable: '--font-mono' });

// Add to body className: `${jakarta.variable} ${jetbrainsMono.variable} font-sans antialiased`
```

## 2. Tailwind v4 `@theme` Overrides (globals.css)
Inject these absolute value mappings. Note that the "background" in glassmorphism must be managed by global layout components, not just a flat hex.

```css
@theme inline {
  --color-foreground: #141414;
  
  --color-primary: #1856FF;
  --color-primary-foreground: #FFFFFF;
  
  --color-secondary: rgba(255, 255, 255, 0.5);
  --color-secondary-foreground: #141414;
  
  --color-muted: rgba(255, 255, 255, 0.3);
  --color-muted-foreground: #3A344E;
  
  --color-border: rgba(255, 255, 255, 0.2);
  --color-ring: #1856FF;
  
  --font-sans: var(--font-sans), ui-sans-serif, system-ui;
  --font-mono: var(--font-mono), ui-monospace, SFMono-Regular;
  
  --radius-lg: 1rem;
  --radius-md: calc(1rem - 4px);
  --radius-sm: calc(1rem - 8px);
}

@utility glass-panel {
  background-color: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}

@utility glass-panel-dark {
  background-color: rgba(0, 0, 0, 0.25);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
}
```

## 3. UI Implementation Mandates
*   **The Foundation**: You must establish a fluid, gradient layout or dynamic background (Mesh gradients, animated blobs, or high-res imagery) for the glass to actually "blur" against. A plain white background defeats glassmorphism.
*   **Cards & Modals**: Do not use standard Shadcn `bg-card`; override them explicitly using the custom `@utility glass-panel` applied via `className="glass-panel"`.
*   **Contrast Warnings**: Glass over light areas renders text invisible. Always ensure `text-foreground` or explicit high-contrast colors exist against the blurred background logic, enforcing WCAG 4.5:1.
