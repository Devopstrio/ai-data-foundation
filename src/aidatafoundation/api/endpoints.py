from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from aidatafoundation.core.engine import DataFoundationEngine
from aidatafoundation.models.schemas import IngestRequest, IngestResponse, SearchRequest, SearchResponse, SearchResult
from aidatafoundation.storage.vector_adapter import VectorStorageAdapter

router = APIRouter()

async def get_engine() -> AsyncGenerator[DataFoundationEngine, None]:
    # In production, use singleton DB connections
    db = VectorStorageAdapter("mock://vector-db:5432")
    engine = DataFoundationEngine(db)
    yield engine

@router.post("/ingest", response_model=IngestResponse)
async def ingest_data(
    req: IngestRequest,
    engine: Annotated[DataFoundationEngine, Depends(get_engine)]
) -> IngestResponse:
    try:
        result = await engine.ingest_document(req.source_id, req.content, req.metadata)
        return IngestResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/search", response_model=SearchResponse)
async def search_data(
    req: SearchRequest,
    engine: Annotated[DataFoundationEngine, Depends(get_engine)]
) -> SearchResponse:
    try:
        raw_results = await engine.search_rag_context(req.query, req.top_k)
        results = [SearchResult(**r) for r in raw_results]
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
