# DocTalk - AI Document Chat Application

🚀 Simple and powerful web application for intelligent conversations with your documents using Azure Computer Vision OCR and Google Gemini AI.

## ✨ Features

- 📁 **Multi-format Upload**: PDF, TXT, DOCX, Images (PNG, JPG, JPEG)
- 🔍 **Smart OCR**: Azure Computer Vision for text extraction from images
- 🧠 **AI Conversations**: Context-aware chat with Google Gemini 2.0 Flash
- 📊 **Document Summarization**: Get comprehensive summaries across all uploaded files
- 🔒 **Session Privacy**: Data automatically deleted when session ends
- 🎨 **Clean UI**: Dark theme with professional interface
- 📥 **Export Options**: Download chat history as TXT or PDF
- ⚡ **Fast Processing**: Vector embeddings for quick document retrieval

## 🛠️ Tech Stack

### Frontend
- **React 18** + Vite
- **Tailwind CSS** 
- **Axios** for API calls

### Backend
- **FastAPI** (High-performance Python API)
- **LangChain** (Document processing)
- **FAISS** (Vector similarity search)
- **Azure Computer Vision** (OCR)
- **Google Gemini 2.0 Flash** (AI responses)
- **ReportLab** (PDF generation)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Sourabsb/DocTalk.git
cd DocTalk
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `backend/.env`:
```env
AZURE_VISION_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_VISION_KEY=your_azure_vision_key
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Frontend Setup
```bash
cd frontend
npm install
```

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

### 5. Run Application
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

Visit **http://localhost:3000** to start using DocTalk! 🎉

## 📖 Usage

1. **Upload Documents**: Select or drag & drop files (PDF, TXT, DOCX, Images)
2. **Wait for Processing**: Files are processed with OCR and vector embeddings
3. **Start Chatting**: Ask questions about your documents
4. **Get Summaries**: Type "summarize" to get comprehensive document summaries
5. **Download History**: Export your conversation as TXT or PDF

## 🚀 Deployment

This project can be deployed on **Render** for both frontend and backend services.

## 📁 Project Structure
```
Chat/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py      # Application entry point
│   │   ├── config.py    # Configuration settings
│   │   ├── models/      # Pydantic schemas
│   │   ├── routes/      # API endpoints
│   │   ├── sessions/    # Session management
│   │   └── utils/       # Core utilities
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment variables
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── styles/      # CSS styling
│   │   └── utils/       # Frontend utilities
│   ├── package.json    # Node dependencies
│   └── .env           # Frontend environment
└── README.md          # This file
```

## 🔧 API Endpoints

- `POST /api/upload` - Upload and process documents
- `POST /api/chat/{session_id}` - Chat with documents
- `POST /api/download` - Export chat history

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ using React, FastAPI, and Google Gemini AI**
