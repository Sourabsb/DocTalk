import React, { useState, useEffect } from 'react'
import FileUpload from './components/FileUpload'
import ChatInterface from './components/ChatInterface'
import Header from './components/Header'

function App() {
  const [sessionId, setSessionId] = useState(() => {
    // Get session from localStorage on initial load
    return localStorage.getItem('chatSessionId') || null
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [downloadHandler, setDownloadHandler] = useState(null)

  // Save session to localStorage whenever it changes
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('chatSessionId', sessionId)
    } else {
      localStorage.removeItem('chatSessionId')
    }
  }, [sessionId])

  const handleUploadSuccess = (newSessionId) => {
    setSessionId(newSessionId)
    setIsProcessing(false)
  }

  const handleNewSession = () => {
    setSessionId(null)
    setIsProcessing(false)
    setDownloadHandler(null)
  }

  const handleSetDownloadHandler = (handler) => {
    setDownloadHandler(() => handler)
  }

  return (
    <div className="min-h-screen bg-gray-900">
      {!sessionId ? (
        <div>
          <Header onNewSession={handleNewSession} />
          <FileUpload 
            onUploadSuccess={handleUploadSuccess}
            isProcessing={isProcessing}
            setIsProcessing={setIsProcessing}
          />
        </div>
      ) : (
        <div className="h-screen flex flex-col bg-gray-900 font-sans">
          <Header 
            onNewSession={handleNewSession} 
            sessionId={sessionId}
            onDownload={downloadHandler}
          />
          <div className="flex-1 overflow-hidden">
            <ChatInterface 
              sessionId={sessionId} 
              onSetDownloadHandler={handleSetDownloadHandler}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default App
