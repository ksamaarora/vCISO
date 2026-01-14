# vciso-backend/app/services/rag_service.py
from typing import List, Dict, Any, Optional
import logging
from app.core.embeddings import EmbeddingService
from app.core.vector_db import VectorDBService
from app.config import settings

logger = logging.getLogger(__name__)

class RAGService:
    """Retrieval-Augmented Generation service for framework guidance"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db = VectorDBService()
        self.top_k = settings.RAG_TOP_K
        self.similarity_threshold = settings.RAG_SIMILARITY_THRESHOLD
    
    async def retrieve_relevant_guidance(
        self,
        query: str,
        framework: Optional[str] = None,
        top_k: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant framework guidance for a query
        
        Args:
            query: The user's query (e.g., "Ransomware response procedures")
            framework: Optional filter by framework (e.g., "NIST SP 800-61")
            top_k: Number of chunks to retrieve (default from config)
        
        Returns:
            List of relevant chunks with metadata and citations
        """
        if top_k is None:
            top_k = self.top_k
        
        try:
            # Generate embedding for the query
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Build filter if framework is specified
            filter_metadata = {"source": framework} if framework else None
            
            # Query vector database
            results = await self.vector_db.query(
                query_vector=query_embedding,
                top_k=top_k,
                filter_metadata=filter_metadata
            )
            
            # Filter by similarity threshold
            filtered_results = [
                r for r in results 
                if r["score"] >= self.similarity_threshold
            ]
            
            if not filtered_results:
                logger.warning(f"No results above threshold {self.similarity_threshold} for query: {query}")
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error retrieving guidance: {e}")
            raise
    
    def format_retrieved_context(self, results: List[Dict[str, Any]]) -> str:
        """
        Format retrieved chunks into a context string for the LLM
        
        Returns formatted string like:
        
        [1] NIST SP 800-61, Section 3.2 (Page 15):
        "Incident response procedures should include..."
        
        [2] CISA Guidelines, Section 2.1 (Page 8):
        "Organizations must implement containment strategies..."
        """
        if not results:
            return "No relevant framework guidance found."
        
        context_parts = []
        for idx, result in enumerate(results, 1):
            metadata = result["metadata"]
            source = metadata.get("source", "Unknown")
            section = metadata.get("section", "Unknown Section")
            page = metadata.get("page", "N/A")
            text = metadata.get("text", "")
            score = result["score"]
            
            citation = f"[{idx}] {source}, {section} (Page {page}) [Relevance: {score:.2f}]:\n\"{text}\"\n"
            context_parts.append(citation)
        
        return "\n\n".join(context_parts)