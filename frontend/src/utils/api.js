import axios from 'axios'

const API_BASE_URL = 'https://doctalk-production.up.railway.app'

const api = axios.create({
  baseURL: API_BASE_URL,
})

export const uploadFiles = async (files) => {
  const formData = new FormData()
  files.forEach(file => {
    formData.append('files', file)
  })

  const response = await api.post('/api/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

export const sendMessage = async (sessionId, message) => {
  const response = await api.post('/api/chat', {
    session_id: sessionId,
    message: message,
  })
  
  return response.data
}

export const downloadChat = async (sessionId, format = 'txt') => {
  const response = await api.post('/api/download', {
    session_id: sessionId,
    format: format,
  }, {
    responseType: 'blob',
  })
  
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `chat_history.${format}`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
