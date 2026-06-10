"""标签管理API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db, Tag
from app.models.schemas import TagResponse, TagCreate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=List[TagResponse])
def list_tags(db: Session = Depends(get_db)):
    """获取所有标签"""
    tags = db.query(Tag).all()
    return [
        TagResponse(
            id=tag.id,
            name=tag.name,
            color=tag.color,
            created_at=tag.created_at
        )
        for tag in tags
    ]


@router.post("", response_model=TagResponse)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """创建标签"""
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="标签已存在")
    
    new_tag = Tag(name=tag.name, color=tag.color)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    
    return TagResponse(
        id=new_tag.id,
        name=new_tag.name,
        color=new_tag.color,
        created_at=new_tag.created_at
    )


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """删除标签"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    db.delete(tag)
    db.commit()
    
    return {"message": "标签已删除"}