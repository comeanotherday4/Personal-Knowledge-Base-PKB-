import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 文档相关API
export const uploadDocument = async (formData) => {
  const response = await api.post('/api/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getDocuments = async (params = {}) => {
  const response = await api.get('/api/documents', { params })
  return response.data
}

export const getDocument = async (id) => {
  const response = await api.get(`/api/documents/${id}`)
  return response.data
}

export const deleteDocument = async (id) => {
  const response = await api.delete(`/api/documents/${id}`)
  return response.data
}

export const updateDocumentTags = async (id, tags) => {
  const response = await api.put(`/api/documents/${id}/tags`, tags)
  return response.data
}

export const suggestTags = async (id) => {
  const response = await api.post(`/api/documents/${id}/suggest-tags`)
  return response.data
}

export const getSimilarDocuments = async (id, limit = 5) => {
  const response = await api.get(`/api/documents/${id}/similar`, { params: { limit } })
  return response.data
}

// 搜索相关API
export const search = async (data) => {
  const response = await api.post('/api/search', data)
  return response.data
}

export const answerQuestion = async (data) => {
  const response = await api.post('/api/search/answer', data)
  return response.data
}

export const suggestSearch = async (query, limit = 5) => {
  const response = await api.get('/api/search/suggest', { params: { query, limit } })
  return response.data
}

// AI相关API
export const generateContent = async (data) => {
  const response = await api.post('/api/ai/generate', data)
  return response.data
}

export const extractKnowledge = async (documentId) => {
  const response = await api.post('/api/ai/extract-knowledge', { document_id: documentId })
  return response.data
}

export const summarizeDocument = async (id) => {
  const response = await api.post(`/api/ai/summarize/${id}`)
  return response.data
}

export const getKnowledgePoints = async (documentId) => {
  const response = await api.get(`/api/ai/knowledge-points/${documentId}`)
  return response.data
}

// 标签相关API
export const getTags = async () => {
  const response = await api.get('/api/tags')
  return response.data
}

export const createTag = async (data) => {
  const response = await api.post('/api/tags', data)
  return response.data
}

export const deleteTag = async (id) => {
  const response = await api.delete(`/api/tags/${id}`)
  return response.data
}

export default {
  uploadDocument,
  getDocuments,
  getDocument,
  deleteDocument,
  updateDocumentTags,
  suggestTags,
  getSimilarDocuments,
  search,
  answerQuestion,
  suggestSearch,
  generateContent,
  extractKnowledge,
  summarizeDocument,
  getKnowledgePoints,
  getTags,
  createTag,
  deleteTag,
}