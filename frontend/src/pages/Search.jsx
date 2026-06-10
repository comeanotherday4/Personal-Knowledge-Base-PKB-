import React, { useState } from 'react'
import { toast } from 'react-toastify'
import api from '../services/api'

function Search() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchType, setSearchType] = useState('search') // search or answer
  
  const handleSearch = async () => {
    if (!query.trim()) {
      toast.warning('请输入搜索内容')
      return
    }
    
    setLoading(true)
    try {
      let response
      if (searchType === 'search') {
        response = await api.search({ query, limit: 10 })
        setResults(response.results.map(r => ({
          ...r,
          type: 'result'
        })))
      } else {
        response = await api.answerQuestion({ query, limit: 5 })
        setResults([{
          type: 'answer',
          answer: response.answer,
          sources: response.sources
        }])
      }
    } catch (error) {
      toast.error('搜索失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }
  
  return (
    <div>
      <div className="card">
        <h2>🔍 知识检索</h2>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ marginRight: '20px' }}>
            <input
              type="radio"
              name="searchType"
              value="search"
              checked={searchType === 'search'}
              onChange={(e) => setSearchType(e.target.value)}
            />
            <span style={{ marginLeft: '5px' }}>语义搜索</span>
          </label>
          <label>
            <input
              type="radio"
              name="searchType"
              value="answer"
              checked={searchType === 'answer'}
              onChange={(e) => setSearchType(e.target.value)}
            />
            <span style={{ marginLeft: '5px' }}>智能问答</span>
          </label>
        </div>
        <div className="search-box">
          <input
            type="text"
            className="search-input"
            placeholder={searchType === 'search' ? '输入关键词或问题进行语义搜索...' : '输入问题，AI将基于知识库回答...'}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <button className="btn btn-primary" onClick={handleSearch} disabled={loading}>
            {loading ? '搜索中...' : '搜索'}
          </button>
        </div>
      </div>
      
      <div className="card">
        <h2>📊 搜索结果</h2>
        {loading ? (
          <div className="loading">搜索中...</div>
        ) : results.length === 0 ? (
          <p style={{ color: '#999', textAlign: 'center', padding: '40px' }}>
            输入关键词开始搜索
          </p>
        ) : (
          <div className="search-results">
            {results.map((result, index) => (
              <div key={index} className="result-item">
                {result.type === 'answer' ? (
                  <>
                    <h3>💡 AI 回答</h3>
                    <p style={{ lineHeight: '1.8', marginBottom: '15px' }}>
                      {result.answer}
                    </p>
                    {result.sources && result.sources.length > 0 && (
                      <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #e0e0e0' }}>
                        <strong>参考来源：</strong>
                        {result.sources.map((source, i) => (
                          <div key={i} style={{ fontSize: '13px', color: '#666', marginTop: '5px' }}>
                            • {source.filename} (相关度: {(source.relevance * 100).toFixed(1)}%)
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                ) : (
                  <>
                    <h3>📄 {result.filename}</h3>
                    <p>{result.highlights && result.highlights[0]}</p>
                    <div style={{ marginTop: '10px', fontSize: '13px', color: '#666' }}>
                      相关度: {(result.score * 100).toFixed(1)}%
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Search