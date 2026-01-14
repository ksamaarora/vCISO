# test_rag.py
import asyncio
from app.services.rag_service import RAGService

async def test_retrieval():
    rag = RAGService()
    
    results = await rag.retrieve_relevant_guidance(
        query="What are the steps for ransomware containment?",
        top_k=3
    )
    
    print("\nRetrieved Guidance:")
    for idx, result in enumerate(results, 1):
        print(f"\n[{idx}] {result['metadata']['source']} (Score: {result['score']:.2f})")
        print(f"Text: {result['metadata']['text'][:200]}...")

if __name__ == "__main__":
    asyncio.run(test_retrieval())