"""工具函数"""
import os
from typing import List
from datetime import datetime


def ensure_dir(directory: str):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def clean_text(text: str) -> str:
    """清理文本"""
    # 移除多余的空白
    text = ' '.join(text.split())
    # 移除特殊字符（保留中文、英文、数字、标点）
    # 这里可以根据需要扩展
    return text.strip()


def split_text_into_chunks(
    text: str, 
    chunk_size: int = 500, 
    overlap: int = 50
) -> List[str]:
    """将文本分割成块"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks


def get_timestamp() -> str:
    """获取时间戳字符串"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def is_valid_file_type(filename: str, allowed_types: List[str]) -> bool:
    """检查文件类型是否允许"""
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in allowed_types