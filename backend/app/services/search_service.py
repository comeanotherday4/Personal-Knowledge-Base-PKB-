"""知识检索服务"""
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models.database import Document, KnowledgePoint
from app.config import get_settings
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
import os

settings = get_settings()


class SearchService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # 初始化ChromaDB
        persist_dir = settings.CHROMA_PERSIST_DIR
        os.makedirs(persist_dir, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(
                anonymized_telemetry=False
            )
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )

    def _get_embedding(self, text: str) -> List[float]:
        """获取文本嵌入向量"""
        embedding = self.model.encode(text)
        return embedding.tolist()

    def index_document(self, document: Document, db: Session):
        """索引文档"""
        if not document.content:
            return
        
        # 分段处理长文档
        chunks = self._split_text(document.content, chunk_size=500, overlap=50)
        
        for i, chunk in enumerate(chunks):
            embedding = self._get_embedding(chunk)
            
            self.collection.add(
                ids=[f"{document.id}_{i}"],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    "document_id": document.id,
                    "filename": document.filename,
                    "chunk_index": i,
                    "file_type": document.file_type
                }]
            )

    def _split_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """分割文本为小块"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks

    def search(
        self, 
        query: str, 
        limit: int = 10,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """搜索知识"""
        query_embedding = self._get_embedding(query)
        
        where_filter = None
        if filters:
            where_filter = {}
            if "file_type" in filters:
                where_filter["file_type"] = filters["file_type"]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i],
                "score": 1 - results['distances'][0][i]  # 转换为相似度分数
            })
        
        return search_results

    def search_by_document(self, query: str, document_id: int, limit: int = 5) -> List[Dict]:
        """在特定文档中搜索"""
        query_embedding = self._get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={"document_id": document_id},
            include=["documents", "metadatas", "distances"]
        )
        
        search_results = []
        for i in range(len(results['ids'][0])):
            search_results.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "score": 1 - results['distances'][0][i]
            })
        
        return search_results

    def delete_document(self, document_id: int):
        """删除文档索引"""
        # 获取所有相关的chunk IDs
        all_items = self.collection.get()
        
        ids_to_delete = []
        for i, metadata in enumerate(all_items['metadatas']):
            if metadata.get('document_id') == document_id:
                ids_to_delete.append(all_items['ids'][i])
        
        if ids_to_delete:
            self.collection.delete(ids=ids_to_delete)

    def get_similar_documents(self, document_id: int, limit: int = 5) -> List[Dict]:
        """获取相似文档"""
        # 获取文档的第一个chunk作为查询
        results = self.collection.get(
            where={"document_id": document_id},
            limit=1,
            include=["embeddings", "documents"]
        )
        
        if not results['ids']:
            return []
        
        query_embedding = results['embeddings'][0]
        
        # 搜索相似文档
        similar = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit + 1,  # +1 因为会包含自己
            include=["documents", "metadatas", "distances"]
        )
        
        similar_docs = []
        seen_doc_ids = set()
        
        for i in range(len(similar['ids'][0])):
            doc_id = similar['metadatas'][0][i].get('document_id')
            if doc_id != document_id and doc_id not in seen_doc_ids:
                seen_doc_ids.add(doc_id)
                similar_docs.append({
                    "document_id": doc_id,
                    "filename": similar['metadatas'][0][i].get('filename'),
                    "content": similar['documents'][0][i],
                    "score": 1 - similar['distances'][0][i]
                })
                
                if len(similar_docs) >= limit:
                    break
        
        return similar_docs