from pydantic import BaseModel, Field
from typing import List

class DocumentPayload(BaseModel):
    document_id: str = Field(..., example="contract_8829_v2")
    raw_text: str = Field(..., example="The governing law for this non-disclosure agreement shall be the laws of Sweden.")
    primary_embedding_model: str = Field(default="text-embedding-005")

class ChunkResponse(BaseModel):
    chunk_id: str
    text_snippet: str
    embedding_dimension: int
    model_used: str

class PipelineResponse(BaseModel):
    document_id: str
    status: str
    chunks_processed: int
    vector_data: List[ChunkResponse]