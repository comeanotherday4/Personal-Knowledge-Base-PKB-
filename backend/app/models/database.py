from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Document(Base):
    """文档模型"""
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    content = Column(Text)
    summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_processed = Column(Boolean, default=False)

    # 关系
    tags = relationship("Tag", secondary="document_tags", back_populates="documents")
    knowledge_points = relationship("KnowledgePoint", back_populates="document")


class Tag(Base):
    """标签模型"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    color = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    documents = relationship("Document", secondary="document_tags", back_populates="tags")


class DocumentTag(Base):
    """文档-标签关联表"""
    __tablename__ = "document_tags"

    document_id = Column(Integer, ForeignKey("documents.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


class KnowledgePoint(Base):
    """知识点模型"""
    __tablename__ = "knowledge_points"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    importance = Column(Integer, default=1)  # 1-5 重要程度
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    document = relationship("Document", back_populates="knowledge_points")
    connections = relationship(
        "KnowledgePoint",
        secondary="knowledge_connections",
        primaryjoin="KnowledgePoint.id==knowledge_connections.c.from_id",
        secondaryjoin="KnowledgePoint.id==knowledge_connections.c.to_id"
    )


class KnowledgeConnection(Base):
    """知识点关联表"""
    __tablename__ = "knowledge_connections"

    from_id = Column(Integer, ForeignKey("knowledge_points.id"), primary_key=True)
    to_id = Column(Integer, ForeignKey("knowledge_points.id"), primary_key=True)
    connection_type = Column(String(50))  # related_to, depends_on, extends, etc.
    strength = Column(Integer, default=1)  # 关联强度 1-5


def init_db():
    """初始化数据库"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()