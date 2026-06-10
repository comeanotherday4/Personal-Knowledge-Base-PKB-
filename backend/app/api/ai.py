"""AI功能API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db, Document, KnowledgePoint
from app.models.schemas import (
    GenerateContentRequest,
    GenerateContentResponse,
    ExtractKnowledgeRequest,
    ExtractKnowledgeResponse,
    KnowledgePointResponse
)
from app.services.ai_service import AIService
from app.services.search_service import SearchService

router = APIRouter(prefix="/ai", tags=["ai"])

ai_service = AIService()
search_service = SearchService()


@router.post("/generate", response_model=GenerateContentResponse)
def generate_content(
    request: GenerateContentRequest,
    db: Session = Depends(get_db)
):
    """基于知识库生成内容"""
    context = []
    
    if request.context_document_ids:
        # 使用指定的文档
        documents = db.query(Document).filter(
            Document.id.in_(request.context_document_ids)
        ).all()
        context = [doc.content for doc in documents if doc.content]
    else:
        # 自动搜索相关文档
        results = search_service.search(request.topic, limit=5)
        for result in results:
            doc_id = result['metadata'].get('document_id')
            if doc_id:
                document = db.query(Document).filter(Document.id == doc_id).first()
                if document and document.content:
                    context.append(document.content)
    
    if not context:
        raise HTTPException(status_code=400, detail="未找到相关内容")
    
    # 生成内容
    content = ai_service.generate_content(
        request.topic,
        context,
        request.style,
        request.length
    )
    
    # 获取来源
    sources = []
    if request.context_document_ids:
        documents = db.query(Document).filter(
            Document.id.in_(request.context_document_ids)
        ).all()
        sources = [doc.filename for doc in documents]
    else:
        results = search_service.search(request.topic, limit=3)
        sources = [r['metadata'].get('filename') for r in results if r['metadata'].get('filename')]
    
    return GenerateContentResponse(
        content=content,
        sources=sources
    )


@router.post("/extract-knowledge", response_model=ExtractKnowledgeResponse)
def extract_knowledge(
    request: ExtractKnowledgeRequest,
    db: Session = Depends(get_db)
):
    """从文档中提取知识点"""
    document = db.query(Document).filter(Document.id == request.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    if not document.content:
        raise HTTPException(status_code=400, detail="文档内容为空")
    
    # 提取知识点
    knowledge_points_data = ai_service.extract_knowledge_points(document.content)
    
    # 保存到数据库
    knowledge_points = []
    for kp_data in knowledge_points_data:
        kp = KnowledgePoint(
            document_id=document.id,
            title=kp_data.get('title', ''),
            content=kp_data.get('content', ''),
            importance=kp_data.get('importance', 1)
        )
        db.add(kp)
        knowledge_points.append(kp)
    
    db.commit()
    
    # 刷新获取ID
    for kp in knowledge_points:
        db.refresh(kp)
    
    # 发现知识点关联
    connections = ai_service.find_connections(knowledge_points_data)
    
    return ExtractKnowledgeResponse(
        knowledge_points=[
            KnowledgePointResponse(
                id=kp.id,
                document_id=kp.document_id,
                title=kp.title,
                content=kp.content,
                importance=kp.importance,
                created_at=kp.created_at
            )
            for kp in knowledge_points
        ],
        connections=connections
    )


@router.post("/summarize/{document_id}")
def summarize_document(document_id: int, db: Session = Depends(get_db)):
    """生成文档摘要"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    if not document.content:
        raise HTTPException(status_code=400, detail="文档内容为空")
    
    summary = ai_service.generate_summary(document.content)
    
    # 保存摘要
    document.summary = summary
    db.commit()
    
    return {"summary": summary}


@router.get("/knowledge-points/{document_id}")
def get_knowledge_points(document_id: int, db: Session = Depends(get_db)):
    """获取文档的知识点"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    knowledge_points = db.query(KnowledgePoint).filter(
        KnowledgePoint.document_id == document_id
    ).all()
    
    return {
        "knowledge_points": [
            {
                "id": kp.id,
                "title": kp.title,
                "content": kp.content,
                "importance": kp.importance,
                "created_at": kp.created_at
            }
            for kp in knowledge_points
        ]
    }