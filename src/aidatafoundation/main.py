import structlog
import uvicorn
from fastapi import FastAPI

from aidatafoundation.api.endpoints import router as data_router

logger = structlog.get_logger()

app = FastAPI(
    title="AI Data Foundation",
    description="Enterprise RAG Pipeline and Vector Store",
    version="1.0.0"
)

app.include_router(data_router, prefix="/v1/data", tags=["Data Foundation"])

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}

def start() -> None:
    logger.info("Starting AI Data Foundation on 0.0.0.0:8015")
    uvicorn.run("aidatafoundation.main:app", host="0.0.0.0", port=8015, reload=True)

if __name__ == "__main__":
    start()
