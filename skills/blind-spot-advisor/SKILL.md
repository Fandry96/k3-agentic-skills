---
name: blind-spot-advisor
description: Surfaces risks, blind spots, and opportunities the operator didn't ask about. Runs after plans are drafted but before execution. Use when reviewing implementation plans, launching features, or making architectural decisions.
---

# Blind Spot Advisor

> **Source:** Atlas UX Proactive Advisor pattern, adapted for K3 Agentic Infrastructure
> **Version:** 1.0
> **Trigger:** Run AFTER an implementation plan is drafted, BEFORE execution begins

## Purpose

GAG executes what's asked. This skill checks what's NOT being asked. It surfaces blind spots across five domains: compliance, conversion, trust, retention, and competitive positioning.

## Execution Protocol

### Step 1: Ingest the Plan

Read the implementation plan or feature spec that was just drafted. Identify:
- What is being built
- Who the target user is
- What data flows are involved
- What external services are touched
- What the deployment target is

### Step 2: Run the Blind Spot Checklist

Evaluate the plan against EVERY item below. For each category, output findings only if a blind spot exists. Skip categories with no findings.

---

## Blind Spot Checklists

### 🔴 Compliance & Legal

- [ ] **Data Privacy (GDPR/CCPA):** Does the feature collect, store, or process PII? Is consent captured and revocable?
- [ ] **Industry Licensing:** Does the feature involve activities that require professional licensure in the target jurisdiction?
- [ ] **Advertising Rules:** Does any AI-generated content constitute advertising? Are required disclosures present?
- [ ] **Data Redistribution:** Does the feature use third-party data (APIs, feeds)? Are redistribution terms verified?
- [ ] **Accessibility (WCAG 2.2 AA):** Does the feature meet minimum accessibility requirements?
- [ ] **Professional Credentials:** Are any professional credentials, certifications, or qualifications accurately and compliantly represented?
- [ ] **CAN-SPAM / Commercial Email:** Does the feature send unsolicited commercial messages?
- [ ] **Terms of Service:** Does the feature comply with third-party platform ToS (APIs, embeds, data providers)?

### 🟢 Conversion & UX

- [ ] **CTA Clarity:** Is there a clear next step on every page/screen?
- [ ] **Mobile Experience:** Has mobile been tested? Is touch target size ≥ 44px?
- [ ] **Page Speed:** Will this addition push LCP above 2.5s?
- [ ] **Form Friction:** Are forms asking for more data than needed at this stage?
- [ ] **Social Proof:** Is there visible trust evidence (reviews, credentials, case studies)?

### 🔵 Retention & Engagement

- [ ] **Notification Strategy:** Will users know when to come back?
- [ ] **Value Frequency:** Does this feature create a reason to return weekly?
- [ ] **Onboarding Gap:** Can a new user understand this without a tutorial?
- [ ] **Churn Signals:** Are we tracking drop-off points?

### ⚪ Competitive & Strategic

- [ ] **Differentiation:** Does this exist on competing realtor sites? If so, what's our edge?
- [ ] **Defensibility:** Can this be copied in a weekend?
- [ ] **Platform Risk:** Are we building on a third-party that could change terms?
- [ ] **Scaling Assumptions:** Does this work at 10x current volume?

---

## Output Format

```markdown
# Blind Spot Advisory — [Plan/Feature Name]

**Reviewed:** [Date]
**Plan Source:** [Link to implementation_plan.md or feature spec]

## 🔴 CRITICAL (Must Address Before Execution)
- [Finding with specific regulatory citation or risk]

## 🟡 HIGH (Should Address Before Launch)
- [Finding with impact assessment]

## 🟢 MEDIUM (Consider for V2)
- [Finding with recommendation]

## 💡 Ideas to Consider
- [Opportunities or enhancements the plan didn't mention]

## ✋ What NOT to Build Yet
- [Features that seem tempting but are premature given current stage]
```

## When to Invoke

| Trigger | Action |
|---------|--------|
| Implementation plan drafted | Run full checklist |
| Feature spec written | Run full checklist |
| PR touches auth, payments, or legal content | Run Compliance section only |
| Jules Day Batch task submitted | Run Compliance + Trust sections |
| Quarterly review | Run full checklist against each active feature |

## Integration with Action-Gating Loop

This skill maps to **Step 2 (VERIFY)** and **Step 3 (SGL GATE)** of the Action-Gating Loop. Findings rated 🔴 CRITICAL should trigger an SGL **REVIEW** or **BLOCK** before execution proceeds.
