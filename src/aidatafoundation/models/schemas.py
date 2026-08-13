
from pydantic import BaseModel


class IngestRequest(BaseModel):
    source_id: str
    content: str
    metadata: dict[str, str]

class IngestResponse(BaseModel):
    status: str
    chunks_created: int
    vector_ids: list[str]

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    chunk_id: str
    source_id: str
    content: str
    score: float

class SearchResponse(BaseModel):
    results: list[SearchResult]
