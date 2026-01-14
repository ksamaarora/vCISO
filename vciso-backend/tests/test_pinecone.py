# test_pinecone.py
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

# Test connection
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# List indexes (should be empty initially)
indexes = pc.list_indexes()
print("✅ Connection successful!")
print(f"Existing indexes: {[idx.name for idx in indexes]}")