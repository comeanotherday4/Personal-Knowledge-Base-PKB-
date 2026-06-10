"""最小化后端启动脚本 - 用于快速测试系统"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建基本的 FastAPI 应用
app = FastAPI(
    title="AI 知识库系统",
    description="个人知识库管理系统 API",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 简单的测试端点
@app.get("/")
async def root():
    return {
        "message": "AI 知识库系统 API",
        "version": "1.0.0",
        "status": "运行中",
        "docs": "访问 /docs 查看 API 文档"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/test")
async def test_endpoint():
    return {"test": "success", "message": "API 正常工作"}

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 AI 知识库系统 - 后端启动")
    print("=" * 60)
    print("📝 API 文档: http://localhost:8000/docs")
    print("🌐 健康检查: http://localhost:8000/health")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
