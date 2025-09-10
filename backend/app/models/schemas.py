from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    sources: List[str]

class UploadResponse(BaseModel):
    message: str
    session_id: str
    processed_files: List[str]

class DownloadRequest(BaseModel):
    session_id: str
    format: str = "txt"
