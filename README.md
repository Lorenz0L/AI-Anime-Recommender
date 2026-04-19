# AI Anime Recommender

Full-stack anime recommender using RAG, Groq LLM, and live MyAnimeList data

## How it works
1. **Groq** analyzes your query and detects mood/themes
2. **ChromaDB** semantic search finds 10 candidate anime
3. **Groq** re-ranks and writes personalized explanations
4. **Jikan API** fetches live MAL scores and community stats.

## Stack
- **Backend:** FastAPI, ChromaDB, HuggingFace sentence-transformers, Groq
- **Frontend:** React, TypeScript, Vite
- **Data:** MyAnimeList via Jikan API (no CSV, always live)

## Setup

### 1. API Keys needed
- **Groq** (free): https://console.groq.com
- **HuggingFace** (free): https://huggingface.co/settings/tokens

### 2. Backend.
```bash
cd backend
python -m venv venv
source venv/bin/activate       
pip install -r requirements.txt
cp .env.example .env            
python -m pipeline.build_pipeline  
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

