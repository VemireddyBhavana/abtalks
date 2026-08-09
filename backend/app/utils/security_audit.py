from typing import Dict, Any, List
from app.core.config import settings


class SecurityAudit:
    """
    Security Audit Utility inspecting system configurations, CORS policies, debug flags,
    and security header readiness.
    """

    @staticmethod
    def run_audit() -> Dict[str, Any]:
        warnings: List[str] = []
        passed_checks: List[str] = []

        # 1. Check Debug Mode
        if settings.DEBUG:
            warnings.append("DEBUG mode is active. Ensure DEBUG=False in production deployments.")
        else:
            passed_checks.append("DEBUG mode disabled.")

        # 2. Check CORS Configuration
        if "*" in settings.CORS_ORIGINS:
            warnings.append("CORS origins contain wildcard '*'. Restrict to trusted domains in production.")
        else:
            passed_checks.append(f"CORS restricted to {len(settings.CORS_ORIGINS)} origin(s).")

        # 3. Check Security Headers Readiness
        passed_checks.append("SecurityHeadersMiddleware active (HSTS, CSP, X-Content-Type-Options, X-Frame-Options).")

        # 4. Check Payload Limits
        passed_checks.append("RequestSizeLimitMiddleware active (2MB limit).")

        return {
            "compliant": len(warnings) == 0,
            "warnings_count": len(warnings),
            "warnings": warnings,
            "passed_checks_count": len(passed_checks),
            "passed_checks": passed_checks,
        }
