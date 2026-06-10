import React, { useState } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'

function AIAssistant() {
  const [topic, setTopic] = useState('')
  const [style, setStyle] = useState('professional')
  const [length, setLength] = useState(500)
  const [generatedContent, setGeneratedContent] = useState('')
  const [loading, setLoading] = useState(false)
  
  const handleGenerate = async () => {
    if (!topic.trim()) {
      toast.warning('请输入主题')
      return
    }
    
    setLoading(true)
    try {
      const response = await api.generateContent({
        topic,
        style,
        length
      })
      setGeneratedContent(response.content)
      toast.success('内容生成成功！')
    } catch (error) {
      toast.error('生成失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div>
      <div className="card">
        <h2>🤖 AI 内容生成助手</h2>
        <p style={{ color: '#666', marginBottom: '20px' }}>
          基于知识库智能生成内容，支持多种风格和长度
        </p>
        
        <div className="form-group">
          <label className="form-label">主题 *</label>
          <input
            type="text"
            className="form-input"
            placeholder="输入要生成内容的主题，例如：人工智能的发展历程"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </div>
        
        <div className="form-group">
          <label className="form-label">风格</label>
          <select 
            className="form-input"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
          >
            <option value="professional">专业严谨</option>
            <option value="casual">轻松易懂</option>
            <option value="academic">学术深入</option>
          </select>
        </div>
        
        <div className="form-group">
          <label className="form-label">字数（约 {length} 字）</label>
          <input
            type="range"
            min="200"
            max="2000"
            step="100"
            value={length}
            onChange={(e) => setLength(parseInt(e.target.value))}
            style={{ width: '100%' }}
          />
        </div>
        
        <button 
          className="btn btn-primary" 
          onClick={handleGenerate}
          disabled={loading}
          style={{ width: '100%' }}
        >
          {loading ? '生成中...' : '✨ 开始生成'}
        </button>
      </div>
      
      {generatedContent && (
        <div className="card">
          <h2>📝 生成的内容</h2>
          <div style={{
            background: '#f9f9f9',
            padding: '20px',
            borderRadius: '8px',
            lineHeight: '1.8',
            whiteSpace: 'pre-wrap'
          }}>
            {generatedContent}
          </div>
          <div style={{ marginTop: '15px' }}>
            <button 
              className="btn btn-secondary"
              onClick={() => {
                navigator.clipboard.writeText(generatedContent)
                toast.success('已复制到剪贴板')
              }}
            >
              📋 复制内容
            </button>
          </div>
        </div>
      )}
      
      <div className="card">
        <h2>💡 使用提示</h2>
        <ul style={{ lineHeight: '2', color: '#666' }}>
          <li>系统会自动从知识库中检索相关内容作为参考</li>
          <li>上传更多相关文档可以提高生成质量</li>
          <li>选择不同的风格可以适应不同的使用场景</li>
          <li>生成的内容可以作为初稿，建议人工审核和修改</li>
        </ul>
      </div>
      
      <div className="card">
        <h2>🎯 其他AI功能</h2>
        <div className="document-list">
          <div className="document-item">
            <div className="document-info">
              <div className="document-title">智能摘要</div>
              <div className="document-meta">自动生成文档摘要</div>
            </div>
            <button className="btn btn-secondary">即将推出</button>
          </div>
          <div className="document-item">
            <div className="document-info">
              <div className="document-title">智能标签</div>
              <div className="document-meta">自动推荐文档标签</div>
            </div>
            <button className="btn btn-secondary">即将推出</button>
          </div>
          <div className="document-item">
            <div className="document-info">
              <div className="document-title">知识问答</div>
              <div className="document-meta">基于知识库回答问题</div>
            </div>
            <button className="btn btn-secondary">即将推出</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AIAssistant