from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# 文档相关
class DocumentBase(BaseModel):
    filename: str
    file_type: str


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    file_path: str
    file_size: int
    content: Optional[str]
    summary: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_processed: bool
    tags: List[str] = []

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    total: int
    documents: List[DocumentResponse]


# 标签相关
class TagBase(BaseModel):
    name: str
    color: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# 知识点相关
class KnowledgePointBase(BaseModel):
    title: str
    content: str
    importance: Optional[int] = 1


class KnowledgePointCreate(KnowledgePointBase):
    document_id: int


class KnowledgePointResponse(KnowledgePointBase):
    id: int
    document_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# 搜索相关
class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 10
    filters: Optional[dict] = None


class SearchResult(BaseModel):
    document_id: int
    filename: str
    content: str
    score: float
    highlights: Optional[List[str]] = None


class SearchResponse(BaseModel):
    total: int
    results: List[SearchResult]


# AI 相关
class GenerateContentRequest(BaseModel):
    topic: str
    context_document_ids: Optional[List[int]] = None
    style: Optional[str] = "professional"  # professional, casual, academic
    length: Optional[int] = 500  # 字数


class GenerateContentResponse(BaseModel):
    content: str
    sources: List[str]


class ExtractKnowledgeRequest(BaseModel):
    document_id: int


class ExtractKnowledgeResponse(BaseModel):
    knowledge_points: List[KnowledgePointResponse]
    connections: List[dict]