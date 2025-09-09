from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.types import LargeBinary
from .database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # New field: store embeddings (as binary blob)
    embedding = Column(LargeBinary, nullable=True)




