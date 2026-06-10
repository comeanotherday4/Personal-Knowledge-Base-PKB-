"""API模块初始化"""
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.ai import router as ai_router
from app.api.tags import router as tags_router

__all__ = [
    "documents_router",
    "search_router",
    "ai_router",
    "tags_router"
]