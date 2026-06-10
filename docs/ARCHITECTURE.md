# 项目架构说明

## 整体架构

本项目采用前后端分离架构，主要包含以下层次：

```
┌─────────────────────────────────────────┐
│          前端层 (React + Vite)           │
│  - 文档管理界面                          │
│  - 知识检索界面                          │
│  - 知识图谱展示                          │
│  - AI助手界面                            │
└─────────────────────────────────────────┘
                    ↓ HTTP/REST API
┌─────────────────────────────────────────┐
│          后端层 (FastAPI)                │
│  - API路由层                             │
│  - 业务逻辑层                            │
│  - 数据访问层                            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          数据层                          │
│  - PostgreSQL (关系型数据)               │
│  - Redis (缓存)                          │
│  - ChromaDB (向量数据库)                 │
│  - 文件系统 (文档存储)                   │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│          AI服务层                        │
│  - OpenAI API                            │
│  - 文档解析                              │
│  - 向量嵌入                              │
│  - 内容生成                              │
└─────────────────────────────────────────┘
```

## 数据流说明

### 1. 文档上传流程
```
用户上传文件 → 前端发送文件 → 后端接收并保存
→ 文档解析服务提取内容 → AI生成摘要
→ 向量嵌入并存储 → 返回处理结果
```

### 2. 知识检索流程
```
用户输入查询 → 向量嵌入 → ChromaDB相似度搜索
→ 获取相关文档片段 → 返回搜索结果
→ (可选)AI生成回答 → 返回完整答案
```

### 3. 内容生成流程
```
用户输入主题 → 搜索相关文档 → 提取上下文
→ AI生成内容 → 返回生成结果
```

## 核心模块说明

### 后端模块

#### 1. API层 (`app/api/`)
负责处理HTTP请求，定义路由和参数验证。

主要API：
- `documents.py`: 文档上传、查询、删除
- `search.py`: 知识检索、问答
- `ai.py`: 内容生成、知识提取
- `tags.py`: 标签管理

#### 2. 服务层 (`app/services/`)
实现核心业务逻辑。

主要服务：
- `FileService`: 文件上传、存储、管理
- `ParserService`: 文档内容解析
- `SearchService`: 向量搜索、相似度计算
- `AIService`: AI功能调用

#### 3. 数据模型层 (`app/models/`)
定义数据结构和数据库映射。

主要模型：
- `Document`: 文档信息
- `Tag`: 标签
- `KnowledgePoint`: 知识点
- `KnowledgeConnection`: 知识关联

### 前端模块

#### 1. 页面组件 (`src/pages/`)
- `Documents`: 文档管理页面
- `Search`: 知识检索页面
- `KnowledgeGraph`: 知识图谱页面
- `AIAssistant`: AI助手页面

#### 2. API服务 (`src/services/api.js`)
封装所有API调用，提供统一的接口。

## 技术选型理由

### 后端技术栈

#### FastAPI
- 高性能异步框架
- 自动API文档生成
- 强类型验证（Pydantic）
- 易于开发和维护

#### PostgreSQL
- 成熟稳定的关系型数据库
- 支持复杂查询
- 数据一致性保证
- 易于扩展

#### ChromaDB
- 轻量级向量数据库
- 易于本地部署
- 支持语义搜索
- 无需额外配置

#### Sentence Transformers
- 开源向量嵌入模型
- 支持多语言
- 本地运行无需API调用
- 性能良好

### 前端技术栈

#### React 18
- 主流前端框架
- 组件化开发
- Hooks简化状态管理
- 生态丰富

#### Vite
- 快速构建工具
- 开发体验好
- 配置简单
- 支持热更新

## 数据模型设计

### Document表
```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    file_size INTEGER,
    content TEXT,
    summary TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_processed BOOLEAN
);
```

### Tag表
```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    color VARCHAR(20),
    created_at TIMESTAMP
);
```

### KnowledgePoint表
```sql
CREATE TABLE knowledge_points (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    title VARCHAR(255),
    content TEXT,
    importance INTEGER,
    created_at TIMESTAMP
);
```

## 性能优化策略

### 1. 文档处理优化
- 异步处理大文件
- 文档分段处理
- 缓存解析结果

### 2. 搜索优化
- 向量索引优化
- 结果缓存
- 分页查询

### 3. 前端优化
- 组件懒加载
- 虚拟滚动
- API请求缓存

## 扩展性设计

### 1. 模块化架构
- API层、服务层、数据层分离
- 易于添加新功能
- 支持插件式扩展

### 2. 配置化设计
- 环境变量管理
- 支持多种AI服务
- 可配置存储方案

### 3. 接口标准化
- RESTful API设计
- 标准响应格式
- 易于集成第三方服务

## 安全设计

### 1. 数据安全
- 文件类型验证
- 文件大小限制
- SQL注入防护

### 2. API安全
- CORS配置
- 请求频率限制
- 认证机制（可扩展）

### 3. 存储安全
- 文件隔离存储
- 数据库访问控制
- 日志审计

## 部署架构

### Docker部署
```
┌──────────────┐
│  Frontend    │ (Nginx容器)
│  Port 3000   │
└──────────────┘
       ↓
┌──────────────┐
│  Backend     │ (FastAPI容器)
│  Port 8000   │
└──────────────┘
       ↓
┌──────────────┐ ┌──────────────┐
│  PostgreSQL  │ │    Redis     │
│  Port 5432   │ │  Port 6379   │
└──────────────┘ └──────────────┘
```

### 本地开发
```
┌──────────────┐
│  Frontend    │ (Vite开发服务器)
│  Port 3000   │
└──────────────┘
       ↓ proxy
┌──────────────┐
│  Backend     │ (Uvicorn)
│  Port 8000   │
└──────────────┘
       ↓
┌──────────────┐ ┌──────────────┐
│  PostgreSQL  │ │    Redis     │
│  (Docker)    │ │   (Docker)   │
└──────────────┘ └──────────────┘
```

## 未来扩展方向

### 1. 功能扩展
- 知识图谱可视化
- 多用户协作
- 知识导入导出
- 移动端支持

### 2. 技术升级
- 微服务架构
- GraphQL API
- 实时通信（WebSocket）
- 分布式存储

### 3. AI增强
- 本地LLM集成
- 模型微调
- 多模态支持
- AI Agent