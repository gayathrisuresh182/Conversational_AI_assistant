"""Long-term memory service for semantic search of past conversations."""
from typing import Dict, Any, List
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from app.config import settings
import json
from datetime import datetime


class LongTermMemory:
    """Service for storing and retrieving long-term conversation memories."""
    
    def __init__(self):
        self.pinecone = Pinecone(api_key=settings.pinecone_api_key)
        self.memory_index_name = f"{settings.pinecone_index_name}-memory"
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure memory index exists."""
        try:
            existing_indexes = self.pinecone.list_indexes()
            index_names = [idx.name for idx in existing_indexes] if hasattr(existing_indexes, '__iter__') else []
            
            if self.memory_index_name not in index_names:
                try:
                    self.pinecone.create_index(
                        name=self.memory_index_name,
                        dimension=384,
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region=settings.pinecone_environment
                        )
                    )
                    print(f"Created Pinecone memory index: {self.memory_index_name}")
                except Exception as create_error:
                    print(f"Note: Memory index creation - {create_error}")
        except Exception as e:
            print(f"Warning: Could not ensure memory index exists: {e}")
            print("Index will be created on first use if it doesn't exist")
    
    def store_memory(self, user_id: str, conversation_text: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Store a conversation memory in the vector database.
        
        Args:
            user_id: User ID
            conversation_text: Text to store
            metadata: Additional metadata
            
        Returns:
            True if successful
        """
        try:
            index = self.pinecone.Index(self.memory_index_name)
            
            # Generate embedding
            embedding = self.embedding_model.encode(conversation_text).tolist()
            
            # Prepare metadata
            memory_metadata = {
                "user_id": user_id,
                "text": conversation_text,
                "timestamp": datetime.utcnow().isoformat(),
                **(metadata or {})
            }
            
            # Generate unique ID
            memory_id = f"{user_id}_{datetime.utcnow().timestamp()}"
            
            # Store in Pinecone
            index.upsert(vectors=[{
                "id": memory_id,
                "values": embedding,
                "metadata": memory_metadata
            }])
            
            return True
            
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False
    
    def search_memories(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant past memories.
        
        Args:
            user_id: User ID
            query: Search query
            top_k: Number of results
            
        Returns:
            List of relevant memories
        """
        try:
            index = self.pinecone.Index(self.memory_index_name)
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter={"user_id": user_id}
            )
            
            # Format results
            memories = []
            for match in results.matches:
                memories.append({
                    "text": match.metadata.get("text", ""),
                    "timestamp": match.metadata.get("timestamp", ""),
                    "score": match.score,
                    "metadata": {k: v for k, v in match.metadata.items() if k not in ["text", "timestamp"]}
                })
            
            return memories
            
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []

