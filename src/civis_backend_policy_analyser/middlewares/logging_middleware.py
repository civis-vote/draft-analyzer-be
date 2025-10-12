import time
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from civis_backend_policy_analyser.config.logging_config import logger

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        path = request.url.path

        # Read request body safely
        try:
            body_bytes = await request.body()
            body = body_bytes.decode("utf-8") if body_bytes else None
        except Exception:
            body = "<Could not read body>"

        logger.info(f"➡️  Incoming request: {method} {path} | Body: {body}")

        try:
            # Process request
            response = await call_next(request)
        except Exception as exc:
            # Log unhandled exception with stack trace
            logger.exception(
                f"💥 Unhandled exception during request: {method} {path}"
            )
            # Return clean 500 response instead of crashing
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )

        # Compute duration
        process_time = (time.time() - start_time) * 1000  # in ms
        status_code = response.status_code

        logger.info(
            f"⬅️  Response: {method} {path} | Status: {status_code} | Time: {process_time:.2f} ms"
        )

        return response
