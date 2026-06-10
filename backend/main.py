"""FastAPI主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import documents, search, ai, tags
from app.models.database import init_db
import uvicorn

# 创建FastAPI应用
app = FastAPI(
    title="AI Native 个人知识库管理系统",
    description="支持文件上传、文档解析、知识检索、知识组织和内容生成的智能知识管理系统",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(documents.router)
app.include_router(search.router)
app.include_router(ai.router)
app.include_router(tags.router)
app.include_router(providers.router)


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    # 初始化数据库
    init_db()
    print("✓ 数据库初始化完成")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "AI Native 个人知识库管理系统",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )