# ⚖️ Legal RAG Ingestion & Resilient Embedding Pipeline
 
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/ShivenSiwach/legal-rag-pipeline)
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)
 
An event-driven FastAPI microservice designed to handle the ingestion, semantic chunking, and vector embedding of large legal documents for Retrieval-Augmented Generation (RAG) applications.
 
---
 
## 📌 1. The Engineering Context
 
In Legal AI, ingesting dense case files and NDAs into vector databases presents significant backend infrastructure challenges. Beyond basic text chunking, scaling a RAG pipeline requires **embedding resilience**.
 
When AI providers deprecate legacy embedding endpoints (e.g., the shutdown of models like `text-embedding-004`), hardcoded ingestion pipelines throw 404 errors, halting vector database updates and breaking downstream legal copilots.
 
This microservice solves this by acting as a shock-absorbing ingestion gateway. It dynamically chunks legal text and includes an automated fallback router that intercepts requests to deprecated embedding models, seamlessly migrating them to active endpoints without pipeline downtime.
 
---
 
## 🏗️ 2. System Architecture
 
```
[Legal PDF / Raw Text] ─────────► [FastAPI Ingestion Gateway]
(Payload: Text, Target Model)         │
                                      ├─► 1. Pydantic Strict Validation
                                      ├─► 2. Semantic Document Chunking
                                      └─► 3. Resilient Routing Engine
                                              │
                                              ▼
                             ┌───────────────────────────────────┐
                             │     Embedding Validation Layer     │
                             ├───────────────────────────────────┤
                             │ Model Active? ──► Generate Vector  │
                             │ Model 404?    ──► Route Fallback   │
                             └───────────────────────────────────┘
```
 
**Stack:**
- **FastAPI** — asynchronous document ingestion gateway
- **Pydantic** — strict payload validation for incoming legal text
- **Semantic Chunking Engine** — splits dense legal documents into coherent retrievable units
- **Resilient Routing Layer** — detects deprecated/404'd embedding models and reroutes to active endpoints automatically
- **Docker** — containerized for deployment alongside legal copilot infrastructure
---
 
## 🧪 3. Live Interactive Demo (No Local Setup Required)
 
You do not need to clone this repository or install Python to test the architecture.
 
1. Click the **[Open in GitHub Codespaces](https://codespaces.new/ShivenSiwach/legal-rag-pipeline)** badge above.
2. The cloud environment will automatically install dependencies and launch the server.
3. Open the forwarded port URL in your browser and append `/docs` to access the interactive Swagger UI.
### Test Payload (Triggering the Fallback Logic)
 
Paste this payload into the `POST /rag/ingest-document` endpoint. Notice we are intentionally requesting a deprecated embedding model (`text-embedding-004`):
 
```json
{
  "document_id": "nda_stockholm_01",
  "raw_text": "This NDA is governed by the laws of Sweden. The receiving party shall not disclose the confidential algorithms. Jurisdiction lies in Stockholm.",
  "primary_embedding_model": "text-embedding-004"
}
```
 
### Expected Output
 
The system successfully chunks the sentences and dynamically routes the embedding request to the active `text-embedding-005` model to prevent a system crash.
 
```json
{
  "document_id": "nda_stockholm_01",
  "status": "successfully_indexed",
  "chunks_processed": 3,
  "vector_data": [
    {
      "chunk_id": "nda_stockholm_01_chunk_0",
      "text_snippet": "This NDA is governed by the laws of Sweden...",
      "embedding_dimension": 768,
      "model_used": "text-embedding-005"
    }
  ]
}
```
 
---
 
## 💻 4. Local Setup & Docker Deployment
 
To deploy this service locally or push to an AWS/GCP container registry:
 
```bash
# 1. Clone repository
git clone https://github.com/ShivenSiwach/legal-rag-pipeline.git
cd legal-rag-pipeline
 
# 2. Build the Docker container
docker build -t legal-rag-pipeline:latest .
 
# 3. Run the containerized service
docker run -d -p 8000:8000 --name rag-ingestion legal-rag-pipeline:latest
 
# 4. Verify health status
curl http://localhost:8000/health
```
 
The API will be live at `http://localhost:8000/docs`.
 
---
 
## 📄 License
 
This project is open-source under the MIT License.
 
---
 
*Architected for resilient AI infrastructure by Shiven Siwach.*