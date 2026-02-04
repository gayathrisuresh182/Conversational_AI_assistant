"""Knowledge base tool for RAG (Retrieval Augmented Generation)."""
from typing import Dict, Any, List
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from app.config import settings
import uuid


class KnowledgeBaseTool:
    """Tool for searching user's uploaded documents using RAG."""
    
    def __init__(self):
        self.pinecone = Pinecone(api_key=settings.pinecone_api_key)
        self.index_name = settings.pinecone_index_name
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure Pinecone index exists, create if not."""
        try:
            # Get list of indexes
            existing_indexes = self.pinecone.list_indexes()
            index_names = [idx.name for idx in existing_indexes] if hasattr(existing_indexes, '__iter__') else []
            
            if self.index_name not in index_names:
                # Create index if it doesn't exist
                try:
                    self.pinecone.create_index(
                        name=self.index_name,
                        dimension=384,  # all-MiniLM-L6-v2 dimension
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region=settings.pinecone_environment
                        )
                    )
                    print(f"Created Pinecone index: {self.index_name}")
                except Exception as create_error:
                    # Index might already exist or creation failed
                    print(f"Note: Index creation - {create_error}")
        except Exception as e:
            print(f"Warning: Could not ensure index exists: {e}")
            print("Index will be created on first use if it doesn't exist")
    
    def search(self, query: str, user_id: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Search user's knowledge base for relevant information.
        
        Args:
            query: Search query
            user_id: User ID to filter results
            top_k: Number of top results to return
            
        Returns:
            Dictionary with search results
        """
        try:
            # Get index
            index = self.pinecone.Index(self.index_name)
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in Pinecone with user filter
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter={"user_id": user_id}
            )
            
            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "text": match.metadata.get("text", ""),
                    "source": match.metadata.get("source", ""),
                    "chunk_index": match.metadata.get("chunk_index", 0),
                    "score": match.score
                })
            
            return {
                "query": query,
                "results": formatted_results,
                "count": len(formatted_results)
            }
            
        except Exception as e:
            return {
                "error": f"Knowledge base search failed: {str(e)}",
                "query": query,
                "results": [],
                "count": 0
            }
    
    def add_document_chunks(self, user_id: str, document_id: str, chunks: List[Dict[str, Any]]) -> bool:
        """
        Add document chunks to the knowledge base.
        
        Args:
            user_id: User ID
            document_id: Document ID
            chunks: List of chunks with text and metadata
            
        Returns:
            True if successful
        """
        try:
            index = self.pinecone.Index(self.index_name)
            
            # Generate embeddings for all chunks
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedding_model.encode(texts).tolist()
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = f"{document_id}_chunk_{i}"
                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "user_id": user_id,
                        "document_id": document_id,
                        "text": chunk["text"],
                        "source": chunk.get("source", ""),
                        "chunk_index": chunk.get("chunk_index", i)
                    }
                })
            
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                index.upsert(vectors=batch)
            
            return True
            
        except Exception as e:
            print(f"Error adding document chunks: {e}")
            return False
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for Claude function calling."""
        return {
            "name": "search_knowledge_base",
            "description": "Search through the user's uploaded documents and knowledge base. Use this when the user asks about their documents, files, or any information they've previously uploaded.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find relevant information in user's documents"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of top results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }

