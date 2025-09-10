from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer
import numpy as np
from .. import models, schemas
from database import SessionLocal

router = APIRouter(prefix="/memories", tags=["Memories"])

# Load embedding model (lightweight model for speed)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.MemoryResponse)
def create_memory(memory: schemas.MemoryCreate, db: Session = Depends(get_db)):
    # Create embedding
    embedding = model.encode(memory.content)
    embedding_bytes = embedding.tobytes()

    new_memory = models.Memory(content=memory.content, embedding=embedding_bytes)
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)
    return new_memory

@router.get("/", response_model=list[schemas.MemoryResponse])
def get_memories(db: Session = Depends(get_db)):
    return db.query(models.Memory).all()

# ✅ Updated to accept JSON body for search
@router.post("/search", response_model=list[schemas.MemoryResponse])
def search_memories(payload: schemas.MemorySearch, db: Session = Depends(get_db)):
    query = payload.query  # extract from body

    # Encode query
    query_embedding = model.encode(query)

    # Fetch all memories
    memories = db.query(models.Memory).all()
    if not memories:
        return []

    # Compute similarity
    results = []
    for m in memories:
        if m.embedding:
            memory_embedding = np.frombuffer(m.embedding, dtype=np.float32)
            similarity = np.dot(query_embedding, memory_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(memory_embedding)
            )
            results.append((m, similarity))

    # Sort by similarity
    results.sort(key=lambda x: x[1], reverse=True)

    return [m for m, _ in results[:5]]  # return top 5
# top 5 matches
