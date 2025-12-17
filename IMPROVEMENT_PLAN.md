# LMS Demo Improvement Plan

## Product & UX
- Clarify primary user journeys (quote → plan → execute → report) with a guided “Getting Started” checklist on the dashboard.
- Add demo data reload/reset button in the sidebar to guarantee populated views when landing deep-linked pages first.
- Provide per-page empty states with quick actions (e.g., “Create TRF”, “Register Sample”) and sample cards/table toggle.
- Unify page headers and spacing; ensure logo/title alignment and consistent iconography.
- Add search/filter on key lists (Projects, TRFs, Samples, Documents, NCRs, Certifications).
- Provide quick links from dashboard metrics to filtered views (e.g., “Critical NCRs”, “Expiring Certifications”).
- Surface timeline widgets: upcoming audits, expiring certs, pending TRFs, scheduled tests.
- Add a dark mode toggle and improve mobile/portrait breakpoints for Streamlit layout.

## Data & Demo Reliability
- Centralize seeding + manual “Reload demo data” action to avoid empty pages; ensure session_state is initialized on every page load.
- Expand demo data for test executions (with timestamps and outcomes) to drive the Test Results page.
- Add cross-links: TRFs → Projects/Test Plans; Samples → Projects/Test Plans; Documents → TRFs/Test Plans/Projects.
- Include realistic file metadata for Documents (size/type) and download stubs.
- Add more statuses and lifecycle timestamps (created/updated/closed) for NCRs, Audits, Certifications.
- Provide fake attachments/URLs for reports and certificates to demo download flows.

## Functionality
- Implement basic CRUD where missing: edit/close NCRs, update audit findings, renew certifications, upload documents.
- Add bulk actions: mark samples as tested/returned; close multiple NCRs; approve multiple TRFs.
- Add notifications/toasts when key thresholds hit (critical NCRs, expiring certs ≤90 days, overdue audits).
- Introduce role hints (Admin, QA, Engineer, Sales) and show which actions each can perform (even if not fully enforced).
- Add “Print/Export PDF” stubs for reports, TRFs, and certificates.

## Observability & Quality
- Add logging for demo actions (who clicked what) and show a small activity feed on the dashboard.
- Include basic input validation and required-field highlights across all forms.
- Add synthetic tests (unit + Streamlit e2e via Playwright) to verify seeded data renders and metrics match counts.
- Add lints/formatting (ruff/black/isort) and pre-commit hooks.

## Performance & Structure
- Lazy-load heavy charts; cache derived metrics (e.g., pass-rate aggregation).
- Centralize layout components (header, cards, metrics) into shared helpers to avoid duplication across pages.
- Move style to a single CSS block; use consistent spacing and typography scales.
- Wrap data access with thin adapters to ease future API/backend swap.

## Security & Deployability
- Provide a sample `.streamlit/config.toml` for prod-friendly defaults (e.g., XSRF, CORS settings).
- Document how to run locally vs. containerized; add a simple `Dockerfile`.
- Add a “demo reset” endpoint or button that clears session and reseeds data.

## Docs & Demos
- Add a short “How to demo” guide per page (talk track + success criteria).
- Include screenshots/gifs in README or a `docs/` folder.
- Add a changelog of demo data and features so presenters know what’s new.

