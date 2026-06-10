import React, { useState, useEffect } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'

function KnowledgeGraph() {
  const [documents, setDocuments] = useState([])
  const [selectedDoc, setSelectedDoc] = useState(null)
  const [knowledgePoints, setKnowledgePoints] = useState([])
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    loadDocuments()
  }, [])
  
  const loadDocuments = async () => {
    try {
      const response = await api.getDocuments()
      setDocuments(response.documents)
    } catch (error) {
      toast.error('加载文档失败')
    }
  }
  
  const extractKnowledge = async (docId) => {
    setLoading(true)
    try {
      const response = await api.extractKnowledge(docId)
      setKnowledgePoints(response.knowledge_points)
      toast.success('知识点提取成功！')
    } catch (error) {
      toast.error('提取知识点失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }
  
  const viewKnowledgePoints = async (docId) => {
    setLoading(true)
    try {
      const response = await api.getKnowledgePoints(docId)
      setKnowledgePoints(response.knowledge_points)
    } catch (error) {
      toast.error('加载知识点失败')
    } finally {
      setLoading(false)
    }
  }
  
  const getImportanceColor = (importance) => {
    const colors = ['#4caf50', '#8bc34a', '#ffc107', '#ff9800', '#f44336']
    return colors[importance - 1] || '#999'
  }
  
  return (
    <div>
      <div className="card">
        <h2>🕸️ 知识图谱</h2>
        <p style={{ color: '#666', marginBottom: '20px' }}>
          从文档中提取知识点，构建知识网络，发现知识间的关联关系
        </p>
        
        <div className="document-list">
          {documents.map(doc => (
            <div key={doc.id} className="document-item">
              <div className="document-info">
                <div className="document-title">{doc.filename}</div>
                <div className="document-meta">
                  {doc.file_type.toUpperCase()} • {doc.is_processed ? '已处理' : '未处理'}
                </div>
              </div>
              <div className="document-actions">
                <button 
                  className="btn btn-primary" 
                  onClick={() => extractKnowledge(doc.id)}
                  disabled={loading}
                >
                  提取知识点
                </button>
                <button 
                  className="btn btn-secondary" 
                  onClick={() => viewKnowledgePoints(doc.id)}
                  disabled={loading}
                >
                  查看知识点
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      {knowledgePoints.length > 0 && (
        <div className="card">
          <h2>💡 知识点 ({knowledgePoints.length})</h2>
          <div className="document-list">
            {knowledgePoints.map((kp, index) => (
              <div key={kp.id || index} className="result-item">
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                  <h3 style={{ flex: 1, margin: 0 }}>{kp.title}</h3>
                  <span 
                    style={{ 
                      background: getImportanceColor(kp.importance),
                      color: 'white',
                      padding: '4px 12px',
                      borderRadius: '12px',
                      fontSize: '12px'
                    }}
                  >
                    重要度: {kp.importance}
                  </span>
                </div>
                <p style={{ color: '#666', lineHeight: '1.6' }}>
                  {kp.content}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
      
      <div className="card">
        <h2>📊 知识网络可视化</h2>
        <div className="knowledge-graph" style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          color: '#999'
        }}>
          <div style={{ textAlign: 'center' }}>
            <p style={{ fontSize: '48px', marginBottom: '10px''>🔗</p>
            <p>知识图谱可视化功能开发中...</p>
            <p style={{ fontSize: '13px', marginTop: '10px' }}>
              将支持知识节点关系展示、交互式探索等功能
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default KnowledgeGraph