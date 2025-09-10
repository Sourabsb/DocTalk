import React from 'react'

const Header = ({ onNewSession, sessionId, onDownload }) => {
  return (
        <header className="bg-gray-900 border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-lg font-bold">D</span>
            </div>
            <h1 className="text-xl font-bold text-white">
              DocTalk
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            {sessionId && onDownload && (
              <>
                <button
                  onClick={() => onDownload('txt')}
                  className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                >
                  Export TXT
                </button>
                <button
                  onClick={() => onDownload('pdf')}
                  className="px-3 py-1.5 text-sm text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                >
                  Export PDF
                </button>
              </>
            )}
            <button
              onClick={onNewSession}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-sm"
            >
              New Session
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header