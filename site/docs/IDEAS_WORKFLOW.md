# Ideas Workflow (Public → Pending → Approved)

## Goal
Allow the public to submit ideas while keeping the dashboard **curated, accurate, and safe**.
All ideas are treated as **pending** until reviewed.

## Intake
- Public submit form route:
  - /en/ideas/submit
  - /es/ideas/submit
- Form is configured for **Netlify Forms** (no backend required).
- Required: **name + email** (identity verification).

## Review
1. Review submissions in Netlify dashboard (Forms).
2. Verify identity:
   - If necessary, reply requesting confirmation details.
3. Classify:
   - Content improvement
   - New case file request
   - Source submission
   - Bug/UI issue
   - Other

## Approval + Publishing
- Approved ideas should be manually added to an approved list (future):
  - content/{locale}/ideas/approved/*.md (recommended)
- For now, approval is tracked via Netlify + internal notes.

## Level 3 Gate
- Level 3 remains gated until identity verification.
- Access request email: standuparkansas@gmail.com
