from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import locks, measurements, matching
from app.core.config import settings

app = FastAPI(
    title="AI Lock Selector API",
    description="API для измерения параметров замков и подбора аналогов",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locks.router, prefix="/api/v1/locks", tags=["locks"])
app.include_router(measurements.router, prefix="/api/v1/measure", tags=["measurements"])
app.include_router(matching.router, prefix="/api/v1/match", tags=["matching"])

@app.get("/")
async def root():
    return {"message": "AI Lock Selector API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
