import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'
import Documents from './pages/Documents'
import Search from './pages/Search'
import KnowledgeGraph from './pages/KnowledgeGraph'
import AIAssistant from './pages/AIAssistant'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="header">
          <h1>🧠 AI Native 个人知识库管理系统</h1>
          <p>智能存储、检索、组织和生成知识</p>
        </header>
        
        <div className="container">
          <Navigation />
          
          <Routes>
            <Route path="/" element={<Documents />} />
            <Route path="/search" element={<Search />} />
            <Route path="/knowledge-graph" element={<KnowledgeGraph />} />
            <Route path="/ai-assistant" element={<AIAssistant />} />
          </Routes>
        </div>
        
        <ToastContainer position="top-right" autoClose={3000} />
      </div>
    </Router>
  )
}

function Navigation() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('/')
  
  useEffect(() => {
    setActiveTab(window.location.pathname)
  }, [])
  
  const handleTabClick = (path) => {
    setActiveTab(path)
    navigate(path)
  }
  
  return (
    <div className="nav-tabs">
      <button 
        className={`nav-tab ${activeTab === '/' ? 'active' : ''}`}
        onClick={() => handleTabClick('/')}
      >
        📄 文档管理
      </button>
      <button 
        className={`nav-tab ${activeTab === '/search' ? 'active' : ''}`}
        onClick={() => handleTabClick('/search')}
      >
        🔍 知识检索
      </button>
      <button 
        className={`nav-tab ${activeTab === '/knowledge-graph' ? 'active' : ''}`}
        onClick={() => handleTabClick('/knowledge-graph')}
      >
        🕸️ 知识图谱
      </button>
      <button 
        className={`nav-tab ${activeTab === '/ai-assistant' ? 'active' : ''}`}
        onClick={() => handleTabClick('/ai-assistant')}
      >
        🤖 AI助手
      </button>
    </div>
  )
}

export default App