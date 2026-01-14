# vciso-backend/app/scripts/index_frameworks.py
"""
Script to index framework documents into the vector database.

Usage:
    python -m app.scripts.index_frameworks

This script:
1. Reads PDFs from app/data/frameworks/
2. Splits them into chunks
3. Generates embeddings
4. Uploads to Pinecone
"""

import asyncio
import os
from pathlib import Path
from typing import List, Dict, Any
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib

from app.core.embeddings import EmbeddingService
from app.core.vector_db import VectorDBService
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Framework metadata
FRAMEWORKS = {
    "nist_sp_800_61.pdf": {
        "source": "NIST SP 800-61",
        "full_name": "Computer Security Incident Handling Guide",
        "version": "Revision 2",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf"
    },
    "cisa_guidelines.pdf": {
        "source": "CISA",
        "full_name": "CISA Incident Response Guidelines",
        "version": "2024",
        "url": "https://www.cisa.gov/topics/cybersecurity-best-practices/incident-response"
    },
    "sans_framework.pdf": {
        "source": "SANS",
        "full_name": "SANS Incident Handler's Handbook",
        "version": "Latest",
        "url": "https://www.sans.org/white-papers/incident-handlers-handbook/"
    }
}

class FrameworkIndexer:
    """Index framework documents into vector database"""
    
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_db = VectorDBService()
        self.frameworks_dir = Path("app/data/frameworks")
        
        # Text splitter configuration
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # ~250 words per chunk
            chunk_overlap=200,  # 20% overlap to preserve context
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    async def index_all_frameworks(self):
        """Index all framework PDFs"""
        logger.info("Starting framework indexing...")
        
        # Check if frameworks directory exists
        if not self.frameworks_dir.exists():
            raise FileNotFoundError(
                f"Frameworks directory not found: {self.frameworks_dir}\n"
                f"Please create it and add framework PDFs."
            )
        
        all_vectors = []
        
        for pdf_filename, metadata in FRAMEWORKS.items():
            pdf_path = self.frameworks_dir / pdf_filename
            
            if not pdf_path.exists():
                logger.warning(f"PDF not found: {pdf_path}, skipping...")
                continue
            
            logger.info(f"Processing: {pdf_filename}")
            vectors = await self.process_pdf(pdf_path, metadata)
            all_vectors.extend(vectors)
            logger.info(f"Generated {len(vectors)} vectors from {pdf_filename}")
        
        # Upload to vector database
        logger.info(f"Uploading {len(all_vectors)} vectors to Pinecone...")
        await self.vector_db.upsert_vectors(all_vectors)
        logger.info("Indexing complete!")
    
    async def process_pdf(
        self,
        pdf_path: Path,
        metadata: Dict[str, str]
    ) -> List[Dict[str, Any]]:
        """Process a single PDF and return vectors"""
        
        # Load PDF
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        
        # Split into chunks
        chunks = []
        for page in pages:
            page_chunks = self.text_splitter.split_text(page.page_content)
            for chunk in page_chunks:
                chunks.append({
                    "text": chunk,
                    "page": page.metadata.get("page", 0)
                })
        
        logger.info(f"Split {pdf_path.name} into {len(chunks)} chunks")
        
        # Generate embeddings (batch)
        texts = [chunk["text"] for chunk in chunks]
        embeddings = await self.embedding_service.generate_embeddings_batch(texts)
        
        # Prepare vectors for Pinecone
        vectors = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Generate unique ID
            vector_id = self._generate_vector_id(
                source=metadata["source"],
                page=chunk["page"],
                chunk_idx=idx
            )
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "source": metadata["source"],
                    "full_name": metadata["full_name"],
                    "version": metadata["version"],
                    "url": metadata["url"],
                    "page": chunk["page"],
                    "text": chunk["text"],
                    "chunk_index": idx
                }
            })
        
        return vectors
    
    def _generate_vector_id(self, source: str, page: int, chunk_idx: int) -> str:
        """Generate unique vector ID"""
        raw_id = f"{source}-page{page}-chunk{chunk_idx}"
        # Use hash to ensure consistent IDs
        return hashlib.md5(raw_id.encode()).hexdigest()

async def main():
    """Main indexing function"""
    indexer = FrameworkIndexer()
    
    # Optional: Clear existing index
    # await indexer.vector_db.delete_all()
    
    await indexer.index_all_frameworks()

if __name__ == "__main__":
    asyncio.run(main())