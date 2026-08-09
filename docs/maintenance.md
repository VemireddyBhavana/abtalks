# Production Operational Maintenance Guide

This guide details operational inspection, log monitoring, and maintenance protocols for the **ABTalks AI Interview Agent**.

---

## 🔍 Log Inspection & Monitoring

Log outputs are saved into `backend/logs/`:
- `application.log`: Full system activity.
- `api.log`: Incoming requests and route handling events.
- `error.log`: Exception stack traces and warning events.
- `performance.log`: Latency timing metrics.

---

## 🩺 System Health Diagnostics

In production, run system diagnostics via:
```python
from app.services.health_dashboard import get_health_dashboard_service
from app.utils.security_audit import SecurityAudit

dashboard = get_health_dashboard_service().get_dashboard_status()
audit = SecurityAudit.run_audit()
```

---

## 🔄 Dependency Maintenance & Auditing
Periodically execute security audits for package dependencies:
```bash
# Python dependencies
cd backend && pip audit

# Node.js dependencies
cd frontend && npm audit
```
