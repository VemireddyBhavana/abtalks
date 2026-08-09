# Production Release Checklist

This checklist acts as the mandatory pre-release quality gate before deploying any version of the **ABTalks AI Interview Agent** to production environments.

---

## 📋 Pre-Release Quality Gate

### 1. Test Suite Verification
- [ ] Run `python -m pytest -v` in `backend/` — All 73+ tests pass cleanly (100% pass rate).
- [ ] Run `npm run test` in `frontend/` — All unit and E2E specs pass cleanly.

### 2. Build & Bundle Optimization
- [ ] Run `npm run build` in `frontend/` — Production build succeeds with Rollup manual chunks (`vendor`, `ui`, route chunks).
- [ ] Verify bundle size limits: vendor JS `< 100kB gzip`, UI JS `< 50kB gzip`.

### 3. Environment & Configuration Hygiene
- [ ] Verify `APP_ENV=production` and `DEBUG=False`.
- [ ] Execute `SecurityAudit.run_audit()` — Confirm zero security warnings.
- [ ] Verify CORS origins are restricted to explicit trusted domains (no wildcard `*`).

### 4. System Health & Observability
- [ ] Inspect `HealthDashboardService.get_dashboard_status()` — Return status is `healthy`.
- [ ] Verify logging directory `logs/` contains `application.log`, `api.log`, `error.log`, and `performance.log`.

### 5. Accessibility & UX Verification
- [ ] Keyboard navigation: All controls accessible via `<tab>` and `<enter>`.
- [ ] Visible focus rings: `focus-visible:ring-emerald-400` active on all interactive elements.
- [ ] Reduced motion support: `motion-reduce:transition-none` enforced.

### 6. Continuous Integration (CI)
- [ ] Push changes to GitHub — GitHub Actions CI pipeline passes green across all jobs.
