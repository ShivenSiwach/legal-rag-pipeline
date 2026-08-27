from fastapi import FastAPI, HTTPException
from app.schemas import DocumentPayload, PipelineResponse, ChunkResponse
from app.embeddings import generate_mock_embedding
import uuid

app = FastAPI(
    title="Legal Document RAG Ingestion Pipeline",
    description="Resilient vector embedding microservice for large legal documents.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "service": "Legal RAG Pipeline",
        "status": "online",
        "message": "Append /docs to the URL to access the interactive Swagger UI."
    }

@app.post("/rag/ingest-document", response_model=PipelineResponse)
def ingest_legal_document(payload: DocumentPayload):
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")
    
    # 1. Chunking Logic (Simulating semantic splitting)
    # For this demo, we split by sentences or arbitrary lengths
    text_chunks = [chunk.strip() for chunk in payload.raw_text.split('.') if len(chunk) > 10]
    
    if not text_chunks:
        text_chunks = [payload.raw_text] # Fallback if no periods found

    processed_chunks = []
    
    # 2. Embedding Generation with Fallback
    for i, chunk in enumerate(text_chunks):
        vector, model_used = generate_mock_embedding(chunk, payload.primary_embedding_model)
        
        processed_chunks.append(
            ChunkResponse(
                chunk_id=f"{payload.document_id}_chunk_{i}",
                text_snippet=chunk[:50] + "...",
                embedding_dimension=len(vector),
                model_used=model_used
            )
        )
        
    return PipelineResponse(
        document_id=payload.document_id,
        status="successfully_indexed",
        chunks_processed=len(processed_chunks),
        vector_data=processed_chunks
    )