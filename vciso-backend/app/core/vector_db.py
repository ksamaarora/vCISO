# vciso-backend/app/core/vector_db.py
from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any, Optional
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class VectorDBService:
    """Interface for vector database operations (Pinecone)"""
    
    def __init__(self):
        self.client = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self.dimension = settings.EMBEDDING_DIMENSION
        self._ensure_index_exists()
        self.index = self.client.Index(self.index_name)
    
    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        try:
            existing_indexes = [idx.name for idx in self.client.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"Creating index: {self.index_name}")
                self.client.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
                logger.info(f"Index {self.index_name} created successfully")
        except Exception as e:
            logger.error(f"Error ensuring index exists: {e}")
            raise
    
    async def upsert_vectors(self, vectors: List[Dict[str, Any]]):
        """
        Insert or update vectors in the index
        
        vectors format:
        [
            {
                "id": "nist-section-1",
                "values": [0.1, 0.2, ...],  # Embedding vector
                "metadata": {
                    "source": "NIST SP 800-61",
                    "section": "Incident Response Planning",
                    "text": "Original text chunk...",
                    "page": 12
                }
            },
            ...
        ]
        """
        try:
            self.index.upsert(vectors=vectors)
            logger.info(f"Upserted {len(vectors)} vectors to {self.index_name}")
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            raise
    
    async def query(
        self,
        query_vector: List[float],
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query the vector database
        
        Returns:
        [
            {
                "id": "nist-section-1",
                "score": 0.95,  # Similarity score
                "metadata": {...}
            },
            ...
        ]
        """
        try:
            results = self.index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter_metadata,
                include_metadata=True
            )
            
            return [
                {
                    "id": match.id,
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in results.matches
            ]
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            raise
    
    async def delete_all(self):
        """Delete all vectors from the index (use with caution)"""
        try:
            self.index.delete(delete_all=True)
            logger.info(f"Deleted all vectors from {self.index_name}")
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            raise