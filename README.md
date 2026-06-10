# AI 知识库管理系统

一个基于 FastAPI + 原生前端的个人知识库系统，支持文档上传、智能知识提取、关键词搜索和基于知识库的 AI 对话。

## 核心功能

### 1. 文档管理
- 支持上传 PDF、Word、TXT、Markdown 四种格式
- 自动解析文档内容并分块索引
- 文档列表查看与删除

### 2. 知识搜索
- 关键词匹配搜索（文件名 + 内容）
- 高亮显示匹配到的内容片段
- 支持浏览文档解析后的内容块

### 3. 智能知识库
- 后台线程异步处理，更新知识库不阻塞其他操作
- 自动从文档中提取关键词和关键句子
- 基于字符 n-gram 相似度算法将内容分类到知识单元
- 相似内容自动合并到同一知识单元，避免重复

### 4. AI 对话
- 基于已上传文档的上下文回答问题
- 支持 Markdown 格式渲染（列表、代码块、加粗等）
- 使用硅基流动（SiliconFlow）API 驱动，默认模型 Qwen2.5-7B-Instruct

## 技术亮点

- **后台并行**：使用 `threading` 将知识库更新任务放到独立守护线程，用户可继续上传、搜索、对话
- **智能分类**：关键词重叠率 + 内容 n-gram 相似度双维度评分，自动把内容片段归类或创建新知识单元
- **关键词去重**：双向互斥检查——如果 A 词包含 B 词或 B 词包含 A 词，只保留一个，避免冗余
- **关键句子提取**：按句号/问号/分号等自然边界拆分句子，优先选择包含关键词和数字的完整句子，避免生硬截断
- **零依赖部署**：不依赖 PostgreSQL、Redis、ElasticSearch 等外部服务，所有数据存于内存，开箱即用

## 技术栈

| 层次 | 技术 |
|------|------|
| 后端 | FastAPI + Uvicorn |
| 前端 | 单文件 HTML + 原生 JavaScript + CSS |
| AI 服务 | 硅基流动 SiliconFlow（Qwen/Qwen2.5-7B-Instruct） |
| 文档解析 | PyMuPDF（PDF）、python-docx（Word） |
| HTTP 请求 | requests |
| 配置 | python-dotenv（.env 文件） |

## 快速开始

### 1. 配置 API Key

复制示例文件并编辑：

```bash
cd backend
cp .env.example .env
```

然后打开 `.env`，设置你的API Key：

```env
OPENAI_API_KEY=your_siliconflow_api_key_here
```

> 注： API Key可以在 [硅基流动平台](https://cloud.siliconflow.cn) 获取。

### 3. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 4. 启动服务

```bash
cd backend
python start_full.py
```

启动后在浏览器访问：

- **主界面**：http://localhost:8000
- **API 文档**：http://localhost:8000/docs

## 目录结构

```
rag/
├── backend/                     # 后端代码（主目录）
│   ├── app/                    # 模块化代码（备用结构）
│   │   ├── api/                # API 路由层
│   │   ├── models/             # 数据模型
│   │   ├── services/           # 业务逻辑
│   │   └── utils/              # 工具函数
│   ├── data/                   # 数据目录
│   │   └── chroma/             # 向量数据（预留）
│   ├── uploads/                # 上传文件目录（预留）
│   ├── index.html              # 前端单文件页面
│   ├── start_full.py           # 主入口文件（功能完整）
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example            # 环境变量示例
│   ├── .env                    # 实际配置（需手动创建）
│   └── Dockerfile              # 容器化配置
├── README.md                   # 项目说明
└── .gitignore                  # Git 忽略规则
```

## 常见问题

### Q1: 启动后提示「未配置 API Key，部分功能将受限」？

检查 `backend/.env` 文件是否存在，并且 `OPENAI_API_KEY` 已填写为有效的硅基流动 API Key。配置后需要重启服务。

### Q2: 上传了文档，为什么搜索不到内容？

上传后只是完成了解析和分块。需要点击界面上的 **「更新知识库」** 按钮，触发后台知识提取任务。可通过 `/api/knowledge/status` 查看进度。

### Q3: 支持哪些文档格式？

目前支持 **PDF、Word（.doc/.docx）、TXT、Markdown（.md/.markdown）** 四种。PPT、Excel 等暂不支持。

### Q4: 数据会持久化吗？

当前版本仅测试功能，使用内存存储，重启服务后数据会清空。如需持久化，可以自行扩展为文件存储（JSON/Pickle）或接入轻量级数据库。

### Q5: 如何更换 AI 模型？

在 `start_full.py` 顶部修改 `AI_MODEL` 变量，或者在 `.env` 中配置 `AI_MODEL` 后修改加载逻辑。硅基流动平台支持多个开源模型，可按需切换。
