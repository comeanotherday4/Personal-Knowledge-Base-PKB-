"""文件管理服务"""
import os
import shutil
import hashlib
from typing import Optional, List
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.database import Document, Tag, DocumentTag
from app.config import get_settings
from datetime import datetime

settings = get_settings()


class FileService:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self.max_file_size = settings.MAX_FILE_SIZE
        os.makedirs(self.upload_dir, exist_ok=True)

    def _get_file_hash(self, file_path: str) -> str:
        """计算文件哈希值"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _get_file_type(self, filename: str) -> str:
        """获取文件类型"""
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        type_mapping = {
            "pdf": "pdf",
            "doc": "word",
            "docx": "word",
            "ppt": "powerpoint",
            "pptx": "powerpoint",
            "txt": "text",
            "md": "markdown",
            "html": "html",
            "htm": "html",
        }
        return type_mapping.get(ext, "unknown")

    async def upload_file(
        self, 
        file: UploadFile, 
        db: Session,
        tags: Optional[List[str]] = None
    ) -> Document:
        """上传文件"""
        # 检查文件大小
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > self.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"文件大小超过限制 ({self.max_file_size / 1024 / 1024}MB)"
            )

        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(self.upload_dir, safe_filename)

        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 计算文件哈希
        file_hash = self._get_file_hash(file_path)
        file_type = self._get_file_type(file.filename)

        # 创建文档记录
        document = Document(
            filename=file.filename,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            is_processed=False
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        # 添加标签
        if tags:
            for tag_name in tags:
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                    db.refresh(tag)
                
                document_tag = DocumentTag(
                    document_id=document.id,
                    tag_id=tag.id
                )
                db.add(document_tag)
            db.commit()

        return document

    def get_document(self, document_id: int, db: Session) -> Optional[Document]:
        """获取文档"""
        return db.query(Document).filter(Document.id == document_id).first()

    def list_documents(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        tag: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> tuple:
        """列出文档"""
        query = db.query(Document)
        
        if tag:
            query = query.join(DocumentTag).join(Tag).filter(Tag.name == tag)
        
        if file_type:
            query = query.filter(Document.file_type == file_type)
        
        total = query.count()
        documents = query.order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
        
        return total, documents

    def delete_document(self, document_id: int, db: Session) -> bool:
        """删除文档"""
        document = self.get_document(document_id, db)
        if not document:
            return False
        
        # 删除文件
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # 删除数据库记录
        db.delete(document)
        db.commit()
        
        return True

    def update_document_tags(
        self, 
        document_id: int, 
        tags: List[str], 
        db: Session
    ) -> Optional[Document]:
        """更新文档标签"""
        document = self.get_document(document_id, db)
        if not document:
            return None
        
        # 清除现有标签
        db.query(DocumentTag).filter(DocumentTag.document_id == document_id).delete()
        
        # 添加新标签
        for tag_name in tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            
            document_tag = DocumentTag(
                document_id=document.id,
                tag_id=tag.id
            )
            db.add(document_tag)
        
        db.commit()
        db.refresh(document)
        
        return document