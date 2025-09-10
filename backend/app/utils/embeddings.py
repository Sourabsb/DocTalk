from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from ..config import CHUNK_SIZE, CHUNK_OVERLAP

class EmbeddingProcessor:
    def __init__(self):
        # Use smaller, memory-efficient model for production
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        self.texts = []
        self.metadatas = []
        self.embeddings = None
    
    def create_vector_store(self, text_data: Dict[str, str]):
        texts = []
        metadatas = []
        
        for source, text in text_data.items():
            chunks = self.text_splitter.split_text(text)
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({
                    "source": source,
                    "chunk_id": i
                })
        
        if not texts:
            raise ValueError("No documents to process")
        
        # Create embeddings
        embeddings = self.model.encode(texts)
        
        # Store data
        self.texts = texts
        self.metadatas = metadatas
        self.embeddings = embeddings
        
        return self
    
    def search_similar(self, query: str, k: int = 3) -> List[Dict]:
        if self.embeddings is None:
            return []
            
        query_embedding = self.model.encode([query])
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()
        top_indices = np.argsort(similarities)[::-1]
        
        # Get diverse results - try to include results from different sources
        results = []
        sources_seen = set()
        
        # First pass: get top results from different sources
        for idx in top_indices:
            source = self.metadatas[idx]["source"]
            if source not in sources_seen and len(results) < k:
                results.append({
                    "content": self.texts[idx],
                    "metadata": self.metadatas[idx],
                    "score": float(similarities[idx])
                })
                sources_seen.add(source)
        
        # Second pass: fill remaining slots with best remaining results
        for idx in top_indices:
            if len(results) >= k:
                break
            
            # Check if this result is already included
            is_duplicate = any(
                r["content"] == self.texts[idx] for r in results
            )
            
            if not is_duplicate:
                results.append({
                    "content": self.texts[idx],
                    "metadata": self.metadatas[idx],
                    "score": float(similarities[idx])
                })
        
        return results
