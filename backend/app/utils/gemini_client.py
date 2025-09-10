import google.generativeai as genai
from typing import List, Dict
from ..config import GEMINI_API_KEY

class GeminiClient:
    def __init__(self):
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            raise ValueError("Gemini API key not configured")
    
    async def generate_response(self, query: str, context_docs: List[Dict], chat_history: List[Dict]) -> Dict[str, any]:
        # Check if this is a summarization request
        is_summary_request = any(word in query.lower() for word in [
            'summarize', 'summary', 'summarise', 'sumary', 'brief', 
            'overview', 'gist', 'main points', 'key points', 'highlights'
        ])
        
        context_text = self._format_context(context_docs)
        history_text = self._format_history(chat_history)
        
        if is_summary_request:
            prompt = f"""You are DocTalk AI, a helpful document assistant. The user is asking for a summary of the uploaded documents.

DOCUMENT CONTEXT (from all uploaded files):
{context_text}

CONVERSATION HISTORY:
{history_text}

USER REQUEST: {query}

INSTRUCTIONS FOR SUMMARIZATION:
- Provide a comprehensive summary covering ALL uploaded documents
- Organize by file/document if multiple files are present
- Include key information, main topics, and important details from each document
- Structure the summary clearly with headings or sections for each file
- Mention specific file names when discussing content from each document
- Provide an overall conclusion that ties together insights from all documents
- Be thorough but concise - capture the essence of all uploaded materials

FORMAT:
# Summary of Uploaded Documents

## [Filename 1]
- Key points and main content

## [Filename 2] 
- Key points and main content

## Overall Summary
- Combined insights and conclusions

COMPREHENSIVE SUMMARY:"""
        else:
            prompt = f"""You are DocTalk AI, a helpful document assistant. Answer the user's question based on the provided document context from multiple uploaded files.

DOCUMENT CONTEXT (from multiple files):
{context_text}

CONVERSATION HISTORY:
{history_text}

USER QUESTION: {query}

INSTRUCTIONS:
- Analyze which file(s) contain relevant information for the question
- Answer using information from the most relevant file(s) 
- ALWAYS mention the specific file name(s) in your response
- Use proper citations like "According to [filename]..." or "Based on [filename]..."
- If information comes from multiple files, clearly distinguish which part comes from which file
- If the answer isn't in any of the uploaded documents, say "I don't have information about that in the uploaded documents"
- Keep responses conversational but always cite your sources clearly
- Format multiple sources like: "According to file1.pdf, X is Y. While file2.docx mentions that Z is W."

ANSWER (with clear file citations):"""
        
        try:
            response = self.model.generate_content(prompt)
            sources = self._extract_sources(context_docs)
            
            return {
                "response": response.text,
                "sources": sources
            }
        except Exception as e:
            raise ValueError(f"Failed to generate response: {str(e)}")
    
    def _format_context(self, context_docs: List[Dict]) -> str:
        formatted = []
        for i, doc in enumerate(context_docs, 1):
            source = doc.get('metadata', {}).get('source', 'Unknown')
            content = doc.get('page_content', '')
            formatted.append(f"FILE: {source}\nCONTENT: {content}\n---")
        return "\n\n".join(formatted)
    
    def _format_history(self, chat_history: List[Dict]) -> str:
        if not chat_history:
            return "No previous conversation."
        
        formatted = []
        for entry in chat_history[-5:]:
            formatted.append(f"User: {entry.get('user', '')}")
            formatted.append(f"Assistant: {entry.get('assistant', '')}")
        return "\n".join(formatted)
    
    def _extract_sources(self, context_docs: List[Dict]) -> List[str]:
        sources = set()
        for doc in context_docs:
            source = doc.get('metadata', {}).get('source', 'Unknown')
            sources.add(source)
        return list(sources)
