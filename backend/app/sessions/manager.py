import uuid
import time
from typing import Dict, Any
from ..config import SESSION_TIMEOUT

class SessionData:
    def __init__(self):
        self.vector_store = None
        self.chat_history = []
        self.documents = []
        self.created_at = time.time()
        self.last_accessed = time.time()
    
    def is_expired(self):
        return time.time() - self.last_accessed > SESSION_TIMEOUT
    
    def update_access(self):
        self.last_accessed = time.time()

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
    
    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SessionData()
        self._cleanup_expired()
        return session_id
    
    def get_session(self, session_id: str) -> SessionData:
        if session_id not in self.sessions:
            raise ValueError("Session not found")
        
        session = self.sessions[session_id]
        if session.is_expired():
            del self.sessions[session_id]
            raise ValueError("Session expired")
        
        session.update_access()
        return session
    
    def delete_session(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def _cleanup_expired(self):
        expired_sessions = [
            sid for sid, session in self.sessions.items()
            if session.is_expired()
        ]
        for sid in expired_sessions:
            del self.sessions[sid]
