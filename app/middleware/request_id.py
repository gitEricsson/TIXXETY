import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIdMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next):
		reqid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
		request.state.request_id = reqid
		response: Response = await call_next(request)
		response.headers["X-Request-ID"] = reqid
		return response
