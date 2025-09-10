import React, { useState, useRef, useEffect } from 'react'
import { sendMessage, downloadChat } from '../utils/api'

// Simple markdown renderer function
const renderMarkdown = (text) => {
  if (!text) return text
  
  // Replace **text** with bold
  return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
}

const ChatInterface = ({ sessionId, onSetDownloadHandler }) => {
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      content: 'Documents processed successfully! Ask me anything about your uploaded files.',
      sources: []
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleDownload = async (format) => {
    try {
      await downloadChat(sessionId, format)
    } catch (error) {
      console.error('Download error:', error)
    }
  }

  // Pass download handler to parent on mount
  useEffect(() => {
    if (onSetDownloadHandler) {
      onSetDownloadHandler(handleDownload)
    }
  }, [onSetDownloadHandler])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = { type: 'user', content: input.trim() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await sendMessage(sessionId, input.trim())
      const assistantMessage = {
        type: 'assistant',
        content: response.response,
        sources: response.sources
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        type: 'assistant',
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        sources: []
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white font-sans">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-4xl mx-auto px-4 py-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className="py-8 border-b border-gray-800"
            >
              <div className={`flex space-x-4 ${
                message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}>
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-semibold flex-shrink-0 ${
                  message.type === 'user' ? 'bg-blue-600' : 'bg-green-600'
                }`}>
                  {message.type === 'user' ? 'U' : 'AI'}
                </div>
                
                {/* Message Content */}
                <div className="flex-1 min-w-0">
                  <div className={`text-white leading-relaxed font-sans text-base ${
                    message.type === 'user' ? 'text-right' : 'text-left'
                  }`}>
                    {message.type === 'user' ? (
                      <div className="whitespace-pre-wrap">{message.content}</div>
                    ) : (
                      <div 
                        className="whitespace-pre-wrap"
                        dangerouslySetInnerHTML={{ 
                          __html: renderMarkdown(message.content) 
                        }}
                      />
                    )}
                  </div>
                  {message.sources && message.sources.length > 0 && (
                    <div className={`mt-4 pt-3 border-t border-gray-700 ${
                      message.type === 'user' ? 'text-right' : 'text-left'
                    }`}>
                      <p className="text-sm text-gray-400 font-sans">
                        📄 Sources: {message.sources.join(', ')}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="py-8 border-b border-gray-800">
              <div className="flex space-x-4">
                <div className="w-8 h-8 rounded-full bg-green-600 flex items-center justify-center text-white text-sm font-semibold flex-shrink-0">
                  AI
                </div>
                <div className="flex-1">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area - Fixed at bottom */}
      <div className="sticky bottom-0 bg-gray-900 p-4">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSubmit(e)
                }
              }}
              placeholder="Ask anything about your documents..."
              className="w-full px-4 py-3 pr-12 border border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none overflow-hidden bg-gray-700 text-white font-sans shadow-sm"
              rows="1"
              style={{ minHeight: '48px', maxHeight: '120px' }}
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface
