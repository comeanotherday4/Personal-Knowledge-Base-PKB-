"""搜索API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Document
from app.models.schemas import SearchQuery, SearchResponse, SearchResult
from app.services.search_service import SearchService
from app.services.ai_service import AIService

router = APIRouter(prefix="/search", tags=["search"])

search_service = SearchService()
ai_service = AIService()


@router.post("", response_model=SearchResponse)
def search_knowledge(
    query: SearchQuery,
    db: Session = Depends(get_db)
):
    """搜索知识库"""
    # 向量搜索
    results = search_service.search(
        query.query,
        limit=query.limit,
        filters=query.filters
    )
    
    # 获取文档信息
    search_results = []
    seen_doc_ids = set()
    
    for result in results:
        doc_id = result['metadata'].get('document_id')
        
        if doc_id and doc_id not in seen_doc_ids:
            seen_doc_ids.add(doc_id)
            
            document = db.query(Document).filter(Document.id == doc_id).first()
            if document:
                search_results.append(SearchResult(
                    document_id=doc_id,
                    filename=document.filename,
                    content=result['content'],
                    score=result['score'],
                    highlights=[result['content'][:200] + "..."]
                ))
    
    return SearchResponse(
        total=len(search_results),
        results=search_results
    )


@router.post("/answer")
def answer_question(
    query: SearchQuery,
    db: Session = Depends(get_db)
):
    """基于知识库回答问题"""
    # 搜索相关内容
    results = search_service.search(
        query.query,
        limit=5
    )
    
    # 获取上下文
    context = []
    seen_doc_ids = set()
    
    for result in results:
        doc_id = result['metadata'].get('document_id')
        
        if doc_id and doc_id not in seen_doc_ids:
            seen_doc_ids.add(doc_id)
            
            document = db.query(Document).filter(Document.id == doc_id).first()
            if document:
                context.append({
                    'filename': document.filename,
                    'content': result['content']
                })
    
    # AI回答
    answer = ai_service.answer_question(query.query, context)
    
    return {
        "answer": answer,
        "sources": [
            {
                "document_id": result['metadata'].get('document_id'),
                "filename": result['metadata'].get('filename'),
                "relevance": result['score']
            }
            for result in results[:3]
        ]
    }


@router.get("/suggest")
def suggest_search(query: str, limit: int = 5):
    """搜索建议（自动补全）"""
    # 简单实现：返回相似查询
    # 实际应用中可以使用更复杂的算法或专门的搜索建议服务
    results = search_service.search(query, limit=limit)
    
    suggestions = []
    for result in results:
        # 提取关键词作为建议
        content = result['content']
        words = content.split()[:10]
        suggestion = " ".join(words)
        if suggestion not in suggestions:
            suggestions.append(suggestion)
    
    return {"suggestions": suggestions[:limit]}