"""Security middleware."""
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add security headers to response."""
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' https://fastapi.tiangolo.com; "
            "font-src 'self' https://fonts.googleapis.com; "
            "connect-src 'self'"
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware."""

    def __init__(self, app, calls: int = 100, period: int = 60):
        """Initialize rate limiter."""
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Check rate limit."""
        client_ip = request.client.host
        current_time = time.time()

        self.clients = {
            ip: times
            for ip, times in self.clients.items()
            if any(t > current_time - self.period for t in times)
        }

        client_times = self.clients.get(client_ip, [])
        client_times = [t for t in client_times if t > current_time - self.period]

        if len(client_times) >= self.calls:
            return Response(
                content="Rate limit exceeded",
                status_code=429,
                headers={"Retry-After": str(self.period)},
            )

        client_times.append(current_time)
        self.clients[client_ip] = client_times

        response = await call_next(request)
        return response

