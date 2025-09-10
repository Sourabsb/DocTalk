from fastapi import APIRouter, Request, HTTPException
from ..models.schemas import ChatMessage, ChatResponse
from ..utils.embeddings import EmbeddingProcessor
from ..utils.gemini_client import GeminiClient

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, chat_request: ChatMessage):
    session_manager = request.app.state.session_manager
    
    try:
        session = session_manager.get_session(chat_request.session_id)
        
        if not session.vector_store:
            raise HTTPException(status_code=400, detail="No documents uploaded for this session")
        
        gemini_client = GeminiClient()
        
        # Check if this is a summarization request
        is_summary_request = any(word in chat_request.message.lower() for word in [
            'summarize', 'summary', 'summarise', 'sumary', 'brief', 
            'overview', 'gist', 'main points', 'key points', 'highlights'
        ])
        
        if is_summary_request:
            # For summary requests, get documents from ALL files
            # Use different search terms to get diverse content
            all_docs = []
            search_terms = ["", "introduction", "conclusion", "main", "important", "key", "overview"]
            
            for term in search_terms:
                docs = session.vector_store.search_similar(term, k=20)
                all_docs.extend(docs)
            
            # Group by source file to ensure all files are represented
            source_groups = {}
            for doc in all_docs:
                source = doc["metadata"].get("source", "Unknown")
                if source not in source_groups:
                    source_groups[source] = []
                source_groups[source].append(doc)
            
            # Take substantial content from each file for comprehensive summary
            context_docs = []
            for source, docs in source_groups.items():
                # Take more chunks from each file for summary (up to 8 per file)
                context_docs.extend(docs[:8])
            
            print(f"Summary mode: Using {len(context_docs)} documents from {len(source_groups)} files")
            print(f"Files to summarize: {list(source_groups.keys())}")
            
        else:
            # Regular query - get relevant context from documents
            relevant_docs = session.vector_store.search_similar(chat_request.message, k=15)
            
            # Group results by source file for better citation
            source_groups = {}
            for doc in relevant_docs:
                source = doc["metadata"].get("source", "Unknown")
                if source not in source_groups:
                    source_groups[source] = []
                source_groups[source].append(doc)
            
            print(f"Found {len(relevant_docs)} relevant documents from {len(source_groups)} files")
            print(f"Files involved: {list(source_groups.keys())}")
            
            # Take top results from each file to ensure diverse representation
            context_docs = []
            for source, docs in source_groups.items():
                # Take top 2-3 chunks from each file
                context_docs.extend(docs[:3])
            
            # Limit total context to avoid overwhelming the model
            context_docs = context_docs[:12]
        
        # Convert to expected format
        formatted_context_docs = [
            {
                "page_content": doc["content"],
                "metadata": doc["metadata"]
            }
            for doc in context_docs
        ]
        
        result = await gemini_client.generate_response(
            chat_request.message,
            formatted_context_docs,
            session.chat_history
        )
        
        session.chat_history.append({
            "user": chat_request.message,
            "assistant": result["response"],
            "sources": result["sources"]
        })
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"]
        )
        
    except ValueError as e:
        print(f"Chat error: {e}")  # Add logging
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Chat error: {e}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))
