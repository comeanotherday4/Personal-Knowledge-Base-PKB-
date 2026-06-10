"""文档管理API"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.schemas import (
    DocumentResponse, 
    DocumentListResponse,
    TagResponse,
    TagCreate
)
from app.services.file_service import FileService
from app.services.parser_service import ParserService
from app.services.search_service import SearchService
from app.services.ai_service import AIService

router = APIRouter(prefix="/documents", tags=["documents"])

file_service = FileService()
parser_service = ParserService()
search_service = SearchService()
ai_service = AIService()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    tags: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """上传文档"""
    # 解析标签
    tag_list = tags.split(",") if tags else []
    
    # 上传文件
    document = await file_service.upload_file(file, db, tag_list)
    
    # 解析文档内容
    content = parser_service.parse(document.file_path, document.file_type)
    if content:
        document.content = content
        document.is_processed = True
        db.commit()
        db.refresh(document)
        
        # 索引文档
        search_service.index_document(document, db)
        
        # 生成摘要
        summary = ai_service.generate_summary(content)
        if summary:
            document.summary = summary
            db.commit()
            db.refresh(document)
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        file_path=document.file_path,
        file_type=document.file_type,
        file_size=document.file_size,
        content=document.content,
        summary=document.summary,
        created_at=document.created_at,
        updated_at=document.updated_at,
        is_processed=document.is_processed,
        tags=[tag.name for tag in document.tags]
    )


@router.get("", response_model=DocumentListResponse)
def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    tag: Optional[str] = None,
    file_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取文档列表"""
    total, documents = file_service.list_documents(db, skip, limit, tag, file_type)
    
    return DocumentListResponse(
        total=total,
        documents=[
            DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                file_path=doc.file_path,
                file_type=doc.file_type,
                file_size=doc.file_size,
                content=doc.content,
                summary=doc.summary,
                created_at=doc.created_at,
                updated_at=doc.updated_at,
                is_processed=doc.is_processed,
                tags=[tag.name for tag in doc.tags]
            )
            for doc in documents
        ]
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: int, db: Session = Depends(get_db)):
    """获取单个文档"""
    document = file_service.get_document(document_id, db)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        file_path=document.file_path,
        file_type=document.file_type,
        file_size=document.file_size,
        content=document.content,
        summary=document.summary,
        created_at=document.created_at,
        updated_at=document.updated_at,
        is_processed=document.is_processed,
        tags=[tag.name for tag in document.tags]
    )


@router.delete("/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    """删除文档"""
    # 先删除索引
    search_service.delete_document(document_id)
    
    # 删除文件和数据库记录
    success = file_service.delete_document(document_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    return {"message": "文档已删除"}


@router.put("/{document_id}/tags", response_model=DocumentResponse)
def update_document_tags(
    document_id: int,
    tags: List[str],
    db: Session = Depends(get_db)
):
    """更新文档标签"""
    document = file_service.update_document_tags(document_id, tags, db)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        file_path=document.file_path,
        file_type=document.file_type,
        file_size=document.file_size,
        content=document.content,
        summary=document.summary,
        created_at=document.created_at,
        updated_at=document.updated_at,
        is_processed=document.is_processed,
        tags=[tag.name for tag in document.tags]
    )


@router.post("/{document_id}/suggest-tags")
def suggest_tags(document_id: int, db: Session = Depends(get_db)):
    """智能推荐标签"""
    document = file_service.get_document(document_id, db)
    if not document:
        raise HTTPException(status_code=404, detail="文档不存在")
    
    if not document.content:
        raise HTTPException(status_code=400, detail="文档内容为空")
    
    existing_tags = [tag.name for tag in document.tags]
    suggested_tags = ai_service.suggest_tags(document.content, existing_tags)
    
    return {"suggested_tags": suggested_tags}


@router.get("/{document_id}/similar")
def get_similar_documents(document_id: int, limit: int = 5):
    """获取相似文档"""
    similar_docs = search_service.get_similar_documents(document_id, limit)
    return {"similar_documents": similar_docs}