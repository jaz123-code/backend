from fastapi import FastAPI
# ✅ Correct
from database import Base, engine
from routes import memories
from fastapi.middleware.cors import CORSMiddleware




# Create DB tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Memory Vault API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this later to ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],  # allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

# Include routes
app.include_router(memories.router)

@app.get("/")
def root():
    return {"message": "Welcome to Memory Vault API!"}


