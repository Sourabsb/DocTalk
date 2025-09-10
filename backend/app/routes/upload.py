from fastapi import APIRouter, UploadFile, File, Request, HTTPException
from typing import List
from ..models.schemas import UploadResponse
from ..utils.document_processor import DocumentProcessor
from ..utils.embeddings import EmbeddingProcessor
from ..config import MAX_FILE_SIZE

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_files(request: Request, files: List[UploadFile] = File(...)):
    session_manager = request.app.state.session_manager
    
    try:
        session_id = session_manager.create_session()
        session = session_manager.get_session(session_id)
        
        processor = DocumentProcessor()
        embedding_processor = EmbeddingProcessor()
        
        all_text_data = {}
        processed_files = []
        error_msgs = []
        
        print(f"Received {len(files)} files for processing")
        
        for file in files:
            try:
                print(f"Processing file: {file.filename}, size: {file.size} bytes")
                
                if file.size > MAX_FILE_SIZE:
                    error_msg = f"File {file.filename} too large (max: {MAX_FILE_SIZE/1024/1024}MB)"
                    error_msgs.append(error_msg)
                    print(error_msg)
                    continue
                
                content = await file.read()
                text_data = await processor.process_file(content, file.filename)
                
                if not text_data:
                    error_msg = f"No text could be extracted from {file.filename}"
                    error_msgs.append(error_msg)
                    print(error_msg)
                    continue
                    
                all_text_data.update(text_data)
                processed_files.append(file.filename)
                print(f"Successfully processed {file.filename}")
                
            except Exception as file_error:
                error_msg = f"Error processing {file.filename}: {str(file_error)}"
                error_msgs.append(error_msg)
                print(error_msg)
        
        if not all_text_data:
            if error_msgs:
                raise HTTPException(status_code=400, detail="; ".join(error_msgs))
            else:
                raise HTTPException(status_code=400, detail="No text extracted from files")
        
        try:
            print("Creating vector store...")
            vector_store = embedding_processor.create_vector_store(all_text_data)
            session.vector_store = vector_store
            session.documents = processed_files
            print("Vector store created successfully!")
            
            return UploadResponse(
                message="Files processed successfully",
                session_id=session_id,
                processed_files=processed_files
            )
        except Exception as vector_error:
            print(f"Vector store error: {vector_error}")
            raise HTTPException(status_code=500, detail=f"Error creating vector store: {str(vector_error)}")
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = f"Upload error: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)
