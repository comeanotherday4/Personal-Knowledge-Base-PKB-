import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { toast } from 'react-toastify'
import api from '../services/api'

function Documents() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedDoc, setSelectedDoc] = useState(null)
  const [tags, setTags] = useState('')
  
  const onDrop = useCallback(async (acceptedFiles) => {
    setLoading(true)
    
    for (const file of acceptedFiles) {
      try {
        const formData = new FormData()
        formData.append('file', file)
        if (tags) {
          formData.append('tags', tags)
        }
        
        const response = await api.uploadDocument(formData)
        toast.success(`文档 ${file.name} 上传成功！`)
        loadDocuments()
      } catch (error) {
        toast.error(`上传失败: ${error.message}`)
      }
    }
    
    setLoading(false)
  }, [tags])
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    maxSize: 50 * 1024 * 1024 // 50MB
  })
  
  const loadDocuments = async () => {
    try {
      setLoading(true)
      const response = await api.getDocuments()
      setDocuments(response.documents)
    } catch (error) {
      toast.error('加载文档失败')
    } finally {
      setLoading(false)
    }
  }
  
  const deleteDocument = async (id) => {
    if (!window.confirm('确定要删除这个文档吗？')) return
    
    try {
      await api.deleteDocument(id)
      toast.success('文档已删除')
      loadDocuments()
    } catch (error) {
      toast.error('删除失败')
    }
  }
  
  const viewDocument = async (doc) => {
    try {
      const response = await api.getDocument(doc.id)
      setSelectedDoc(response)
    } catch (error) {
      toast.error('加载文档详情失败')
    }
  }
  
  React.useEffect(() => {
    loadDocuments()
  }, [])
  
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
  }
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('zh-CN')
  }
  
  return (
    <div>
      <div className="card">
        <h2>📤 上传文档</h2>
        <div className="form-group">
          <label className="form-label">标签（可选，用逗号分隔）</label>
          <input
            type="text"
            className="form-input"
            placeholder="例如：技术, AI, 机器学习"
            value={tags}
            onChange={(e) => setTags(e.target.value)}
          />
        </div>
        <div {...getRootProps()} className={`upload-area ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>放开以上传文件...</p>
          ) : (
            <div>
              <p>📁 拖拽文件到这里，或点击选择文件</p>
              <p style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
                支持 PDF、Word、PowerPoint、Markdown、HTML 等格式（最大 50MB）
              </p>
            </div>
          )}
        </div>
      </div>
      
      <div className="card">
        <h2>📚 文档列表 ({documents.length})</h2>
        {loading ? (
          <div className="loading">加载中...</div>
        ) : documents.length === 0 ? (
          <p style={{ color: '#999', textAlign: 'center', padding: '40px' }}>
            暂无文档，请上传文档开始使用
          </p>
        ) : (
          <div className="document-list">
            {documents.map(doc => (
              <div key={doc.id} className="document-item">
                <div className="document-info">
                  <div className="document-title">{doc.filename}</div>
                  <div className="document-meta">
                    {doc.file_type.toUpperCase()} • {formatFileSize(doc.file_size)} • {formatDate(doc.created_at)}
                    {doc.is_processed && <span style={{ color: '#4caf50', marginLeft: '10px' }}>✓ 已处理</span>}
                  </div>
                  {doc.tags && doc.tags.length > 0 && (
                    <div style={{ marginTop: '8px' }}>
                      {doc.tags.map((tag, i) => (
                        <span key={i} className="tag">{tag}</span>
                      ))}
                    </div>
                  )}
                  {doc.summary && (
                    <div style={{ marginTop: '8px', fontSize: '13px', color: '#666' }}>
                      {doc.summary.substring(0, 100)}...
                    </div>
                  )}
                </div>
                <div className="document-actions">
                  <button className="btn btn-secondary" onClick={() => viewDocument(doc)}>
                    查看
                  </button>
                  <button className="btn btn-danger" onClick={() => deleteDocument(doc.id)}>
                    删除
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      {selectedDoc && (
        <div className="modal" onClick={() => setSelectedDoc(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedDoc.filename}</h2>
              <button className="modal-close" onClick={() => setSelectedDoc(null)}>×</button>
            </div>
            <div>
              {selectedDoc.summary && (
                <div className="form-group">
                  <label className="form-label">摘要</label>
                  <p>{selectedDoc.summary}</p>
                </div>
              )}
              <div className="form-group">
                <label className="form-label">内容</label>
                <div style={{ 
                  maxHeight: '400px', 
                  overflow: 'auto', 
                  padding: '15px',
                  background: '#f9f9f9',
                  borderRadius: '5px',
                  whiteSpace: 'pre-wrap'
                }}>
                  {selectedDoc.content || '内容加载中...'}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Documents