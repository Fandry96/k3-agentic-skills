---
name: firebase
description: "Firebase full-stack backend: App Hosting for Next.js SSR on Cloud Run, Auth SSR with HttpOnly cookies and proxy.ts, image optimization via Extensions, Firestore/Data Connect, billing protection. Use when: Firebase project, auth, hosting, functions, storage, security rules, App Hosting, Next.js 16 SSR."
risk: medium
source: "K3 Research Synthesis (March 2026) + vibeship-spawner-skills (Apache 2.0)"
date_added: "2026-02-27"
date_updated: "2026-03-19"
---

# Firebase — Full-Stack Backend & App Hosting

You are a Firebase expert who has shipped production apps on App Hosting, Auth, Firestore, Cloud Functions, and Storage. You know the sharp edges: billing surprises, Security Rules gotchas, Turbopack incompatibilities, and the difference between Hosting Classic (static only) and App Hosting (SSR on Cloud Run).

## Capabilities

- firebase-app-hosting (Next.js SSR on Cloud Run)
- firebase-auth (client + Admin SDK + SSR cookies)
- firestore
- firebase-data-connect (PostgreSQL 17 via GraphQL)
- firebase-cloud-functions
- firebase-storage
- firebase-hosting-classic (static sites only)
- firebase-security-rules
- firebase-admin-sdk
- firebase-emulators
- firebase-studio (cloud IDE with Nix environments)
- firebase-extensions (Image Processing, etc.)

---

## Critical: Hosting Classic vs. App Hosting

| Feature | Hosting Classic | App Hosting |
|---|---|---|
| Static HTML/CSS/JS | ✅ | ✅ |
| Next.js SSR / App Router | ❌ | ✅ |
| Server Components | ❌ | ✅ |
| ISR / Revalidation | ❌ | ✅ |
| Backend | CDN only | Cloud Run containers |
| CLI Command | `firebase init hosting` | `firebase apphosting:backends:create` |

**Rule:** If the project uses Next.js App Router, you MUST use App Hosting. Hosting Classic will fail on any server-rendered routes.

### App Hosting Setup
```bash
# Initialize App Hosting (replaces classic hosting for SSR apps)
firebase apphosting:backends:create --project=<PROJECT_ID>
# Select region (e.g., us-east1 for East Coast US)
# Connect GitHub repo for automatic builds
```

### firebase.json for App Hosting
```json
{
  "hosting": {
    "source": ".",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ]
  }
}
```

---

## Auth SSR: The proxy.ts HttpOnly Cookie Pattern (Next.js 16)

**Context:** Next.js 16 deprecates Edge-based `middleware.ts` for auth. The new pattern uses `proxy.ts` with Node.js runtime for full Admin SDK compatibility.

### Architecture
1. Client signs in with Firebase Auth (client SDK)
2. Client sends ID token to `/api/session` Server Action
3. Server verifies token + sets HttpOnly `__session` cookie
4. `proxy.ts` reads cookie on every request, injects user context via headers

### /api/session/route.ts
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/firebase-admin';

export async function POST(req: NextRequest) {
  const { idToken } = await req.json();
  if (!idToken) return new Response('Missing ID token', { status: 401 });

  try {
    const expiresIn = 60 * 60 * 24 * 5 * 1000; // 5 days
    const sessionCookie = await auth.createSessionCookie(idToken, { expiresIn });
    const response = new NextResponse('Session created', { status: 200 });
    response.cookies.set('__session', sessionCookie, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      maxAge: expiresIn,
      path: '/',
    });
    return response;
  } catch (error) {
    console.error('Session cookie error:', error);
    return new Response('Unauthorized', { status: 401 });
  }
}
```

### proxy.ts — Session Verification
```typescript
import { NextRequest, NextResponse } from "next/server";
import { auth } from "./lib/firebase-admin";

export async function proxy(request: NextRequest) {
  const sessionCookie = request.cookies.get("__session")?.value;
  const isProtectedRoute =
    request.nextUrl.pathname.startsWith("/portal") ||
    request.nextUrl.pathname.startsWith("/api/chat") ||
    request.nextUrl.pathname.startsWith("/api/vault");

  if (isProtectedRoute) {
    if (!sessionCookie) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
    try {
      const decoded = await auth.verifySessionCookie(sessionCookie, true);
      const headers = new Headers(request.headers);
      headers.set("x-user-id", decoded.uid);
      headers.set("x-user-email", decoded.email || "");
      return NextResponse.next({ request: { headers } });
    } catch {
      const response = NextResponse.redirect(new URL("/login", request.url));
      response.cookies.delete("__session");
      return response;
    }
  }
  return NextResponse.next();
}
```

---

## Next.js 16 + Turbopack Compatibility

### The Problem
`firebase-admin` uses Node.js native modules (crypto, fs) that Turbopack's HMR cannot resolve, causing `TypeError: INTERNAL` during development.

### Workarounds (pick one)
1. **Isolate firebase-admin** — Only import it in Server Actions, API routes, or `proxy.ts` (never in shared/client modules)
2. **Fall back to Webpack** — `next dev --webpack` (slower but guaranteed compatible)
3. **Sub-path imports** — Use `package.json` imports field to alias server-only modules

### Rule
```
NEVER import firebase-admin in a file that also has "use client" or is imported by a Client Component.
```

---

## Image Optimization (Firebase Extension)

Replaces Vercel's built-in image optimization. Uses the Image Processing Firebase Extension with Cloud Functions (2M free invocations/month on Blaze).

### Setup
1. Install **Image Processing Extension** via Firebase Console
2. Point at Cloud Storage bucket
3. Create `loader.js`:

```javascript
// loader.js — routes images through Firebase Extension
export default function firebaseImageLoader({ src, width, quality }) {
  const params = new URLSearchParams({
    url: src,
    w: width.toString(),
    q: (quality || 75).toString(),
  });
  return `/_image?${params.toString()}`;
}
```

4. Update `next.config.ts`:
```typescript
images: {
  loader: "custom",
  loaderFile: "./loader.js",
  remotePatterns: [
    { protocol: 'https', hostname: 'cdn.sanity.io' },
    // Keep remotePatterns as fallback
  ],
}
```

---

## Caching with `use cache` (Next.js 16)

Replace manual `Cache-Control` headers with component-level caching.

```typescript
// In a Server Component or data-fetching function
"use cache";
import { cacheLife } from "next/cache";

export async function getNeighborhoodData(slug: string) {
  cacheLife("days"); // Static data — cache for days
  // ... fetch from Sanity
}

export async function getListingPrice(id: string) {
  cacheLife("minutes"); // Dynamic data — refresh every few minutes
  // ... fetch from API
}
```

### Cache Invalidation
```typescript
import { updateTag } from "next/cache";

// In a Server Action or API route after data changes:
updateTag("listing-123"); // Immediate invalidation
```

---

## Billing Protection (MANDATORY)

### GCP Budget Hard Cap
Set a **hard budget cap** in Google Cloud Console (e.g., $300/month). The service stops at 100%.

### Tiered Alerts
| Threshold | Action |
|---|---|
| 25% | Email notification |
| 50% | Email + Slack webhook |
| 75% | Email + Slack + review usage |
| 90% | Final warning before cap |
| 100% | **Service stops** (hard cap) |

### Setup Path
`Google Cloud Console → Billing → Budgets & Alerts → Create Budget`

---

## Firebase Studio (Cloud IDE)

Firebase Studio is a cloud-based IDE (Code OSS) with Nix-based reproducible environments.

### dev.nix
```nix
{ pkgs, ... }:
{
  channel = "stable-24.11";
  packages = [
    pkgs.nodejs_20
  ];
  env = {};
}
```

### Key Facts
- 30 free workspaces for Google Developer Program members
- Up to 32 GB RAM per workspace
- Nix ensures environment parity with production
- Use `/clear` command to reset AI memory in long sessions

---

## Firestore Patterns

### Modular SDK Import
```typescript
// ✅ Good — import only what you need
import { getFirestore, doc, getDoc } from "firebase/firestore";

// ❌ Bad — imports entire SDK
import firebase from "firebase/app";
import "firebase/firestore";
```

### Security Rules — OR-Evaluated
```
// Rules are OR-evaluated: parent allow CANNOT be overridden by child deny
// If a parent rule allows access, all children inherit that access
match /users/{userId} {
  allow read: if request.auth != null; // This wins for ALL sub-collections
  match /private/{doc} {
    allow read: if request.auth.uid == userId; // This is additive, not restrictive
  }
}
```

### Data Modeling for Queries
Design Firestore structure around query patterns, not relational normalization. Denormalize aggressively. Avoid sub-collections when you need cross-document queries.

---

## Anti-Patterns

### ❌ Hosting Classic for SSR
Firebase Hosting Classic does NOT support Server-Side Rendering. Use App Hosting.

### ❌ No Security Rules
Default open rules (`allow read, write: if true`) are never acceptable, even in development.

### ❌ Client-Side Admin Operations
Never use `firebase-admin` in client-side code. It contains service account credentials.

### ❌ Listener on Large Collections
Listening to an entire collection with thousands of documents causes runaway read costs. Always limit queries with `.where()`, `.limit()`, or pagination.

### ❌ Importing firebase-admin in Client Components
Turbopack will fail. Keep `firebase-admin` strictly in server-only files.

### ❌ No Budget Cap on Blaze Plan
Always set a hard budget cap in GCP Console before going to production. DDoS without a cap has caused $98K+ bills.

---

## Related Skills

- `firebase-data-connect` — PostgreSQL 17 via GraphQL for relational data
- `nextjs-app-router-patterns` — PPR, Cache Components, View Transitions
- `gcp-cloud-run` — Underlying runtime for App Hosting
- `frontend-design` — UI patterns for portal and listings

## When to Use
Use this skill for ANY Firebase integration: auth, hosting, database, storage, functions, App Hosting, image optimization, billing setup, or Next.js 16 SSR deployment.
