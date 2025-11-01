from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import api_router
from app.middleware.request_id import RequestIdMiddleware

setup_logging()

app = FastAPI(title=settings.app_name)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)
app.add_middleware(RequestIdMiddleware)

@app.get("/health")
async def health() -> dict:
	return {"status": "ok"}

app.include_router(api_router)
