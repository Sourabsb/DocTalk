from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from ..models.schemas import DownloadRequest
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

router = APIRouter()

@router.post("/download")
async def download_chat(request: Request, download_request: DownloadRequest):
    session_manager = request.app.state.session_manager
    
    try:
        session = session_manager.get_session(download_request.session_id)
        
        if not session.chat_history:
            raise HTTPException(status_code=400, detail="No chat history to download")
        
        if download_request.format == "txt":
            content = _generate_txt_content(session.chat_history)
            return StreamingResponse(
                io.StringIO(content),
                media_type="text/plain",
                headers={"Content-Disposition": "attachment; filename=chat_history.txt"}
            )
        elif download_request.format == "pdf":
            pdf_content = _generate_pdf_content(session.chat_history)
            return StreamingResponse(
                io.BytesIO(pdf_content),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=chat_history.pdf"}
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _generate_txt_content(chat_history):
    content = "Chat History\n" + "="*50 + "\n\n"
    
    for i, entry in enumerate(chat_history, 1):
        content += f"Q{i}: {entry['user']}\n"
        content += f"A{i}: {entry['assistant']}\n"
        if entry.get('sources'):
            content += f"Sources: {', '.join(entry['sources'])}\n"
        content += "\n" + "-"*30 + "\n\n"
    
    return content

def _generate_pdf_content(chat_history):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    y_position = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y_position, "Chat History")
    y_position -= 50
    
    for i, entry in enumerate(chat_history, 1):
        # Check if we need a new page
        if y_position < 120:
            p.showPage()
            y_position = height - 50
        
        # Question section
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, f"Question {i}:")
        y_position -= 20
        
        p.setFont("Helvetica", 10)
        user_lines = _wrap_text(entry['user'], 85)
        for line in user_lines:
            if y_position < 80:
                p.showPage()
                y_position = height - 50
            p.drawString(70, y_position, line)
            y_position -= 14
        
        y_position -= 10
        
        # Answer section
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, y_position, f"Answer {i}:")
        y_position -= 20
        
        p.setFont("Helvetica", 10)
        assistant_lines = _wrap_text(entry['assistant'], 85)
        for line in assistant_lines:
            if y_position < 80:
                p.showPage()
                y_position = height - 50
            p.drawString(70, y_position, line)
            y_position -= 14
        
        # Sources section
        if entry.get('sources'):
            y_position -= 5
            p.setFont("Helvetica-Oblique", 9)
            sources_text = f"Sources: {', '.join(entry['sources'])}"
            sources_lines = _wrap_text(sources_text, 85)
            for line in sources_lines:
                if y_position < 80:
                    p.showPage()
                    y_position = height - 50
                p.drawString(70, y_position, line)
                y_position -= 12
        
        # Add separator
        y_position -= 15
        p.setStrokeColorRGB(0.7, 0.7, 0.7)
        p.line(50, y_position, width - 50, y_position)
        y_position -= 25
    
    p.save()
    buffer.seek(0)
    return buffer.getvalue()

def _wrap_text(text, max_length):
    """Wrap text to fit within specified character length"""
    if not text:
        return [""]
    
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        # Check if adding this word would exceed the limit
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) <= max_length:
            current_line = test_line
        else:
            # If current line has content, add it to lines
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                # Handle very long words
                if len(word) > max_length:
                    # Break long words
                    while len(word) > max_length:
                        lines.append(word[:max_length])
                        word = word[max_length:]
                    current_line = word
                else:
                    current_line = word
    
    # Add the last line if it has content
    if current_line:
        lines.append(current_line)
    
    return lines if lines else [""]
