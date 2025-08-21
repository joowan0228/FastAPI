from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from app.services.auth import AuthService


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        excluded_paths = ["/users", "/users/login", "/users/search"]
        if request.url.path in excluded_paths or request.url.path.startswith("/docs") or request.url.path.startswith(
                "/openapi.json") or request.url.path.startswith("/movies"):
            return await call_next(request)

        try:

            if request.url.path.startswith("/users"):
                request = await AuthService().get_current_user(request)

            response: Response = await call_next(request)
            return response
        except HTTPException as e:
            return JSONResponse({"detail": e.detail}, status_code=e.status_code)
        except Exception as e:

            return JSONResponse({"detail": "An internal server error occurred."}, status_code=500)