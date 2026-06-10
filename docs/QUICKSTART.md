# 快速启动指南

## 第一步：安装必要软件

### 必需软件
1. **Docker Desktop** (推荐)
   - 下载地址: https://www.docker.com/products/docker-desktop
   - 安装后启动Docker Desktop

2. **Python 3.10+** (本地开发需要)
   - 下载地址: https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

3. **Node.js 18+** (本地开发需要)
   - 下载地址: https://nodejs.org/
   - 选择 LTS 版本

### 验证安装
```bash
docker --version
python --version
node --version
```

## 第二步：获取OpenAI API Key

1. 访问 https://platform.openai.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的API Key
5. 复制保存API Key

**注意**: 如果使用其他AI服务（如国内API），修改 `OPENAI_API_BASE` 配置

## 第三步：配置项目

### Docker方式（最简单）

```bash
# 1. 进入项目目录
cd d:\own_project\trae_al_project\rag

# 2. 创建环境变量文件
# Windows PowerShell:
Copy-Item backend\.env.example backend\.env

# 编辑 backend\.env 文件，设置:
# OPENAI_API_KEY=你的API密钥

# 3. 启动所有服务
docker-compose up -d

# 4. 查看服务状态
docker-compose ps

# 5. 查看日志（可选）
docker-compose logs -f backend
```

### 本地开发方式

#### 后端设置
```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 配置环境变量
# Windows PowerShell:
Copy-Item .env.example .env
# 编辑 .env 文件

# 6. 启动数据库（使用Docker）
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=knowledge_base \
  postgres:15-alpine

docker run -d --name redis -p 6379:6379 redis:7-alpine

# 7. 启动后端
python main.py
```

#### 前端设置
```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm start
```

## 第四步：访问应用

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 第五步：开始使用

### 上传第一个文档
1. 打开浏览器访问 http://localhost:3000
2. 点击"文档管理"
3. 拖拽一个PDF或Word文档到上传区域
4. 等待文档处理完成

### 搜索知识
1. 点击"知识检索"
2. 输入关键词或问题
3. 查看搜索结果

### AI内容生成
1. 点击"AI助手"
2. 输入主题（如"人工智能的发展历程"）
3. 选择风格和字数
4. 点击"开始生成"

## 常见问题解决

### 问题1: Docker启动失败
```bash
# 检查Docker状态
docker ps

# 重启服务
docker-compose restart

# 查看错误日志
docker-compose logs
```

### 问题2: 端口被占用
```bash
# 检查端口占用
# Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# 修改 docker-compose.yml 中的端口映射
```

### 问题3: 数据库连接失败
```bash
# 检查数据库容器
docker ps | grep postgres

# 重启数据库
docker-compose restart postgres

# 检查连接配置
# 确保 .env 中的 DATABASE_URL 正确
```

### 问题4: API Key无效
```bash
# 检查 .env 文件
# 确保 OPENAI_API_KEY 正确设置
# 确保没有多余的空格或引号
```

## 停止服务

```bash
# Docker方式
docker-compose down

# 本地开发
# Ctrl+C 停止后端和前端服务
docker stop postgres redis
```

## 数据备份

```bash
# 备份上传的文件
cp -r backend/uploads backup/uploads

# 备份向量数据库
cp -r backend/data backup/data

# Docker数据卷备份
docker-compose exec postgres pg_dump -U postgres knowledge_base > backup.sql
```

## 下一步

- 阅读完整文档: README.md
- 查看API文档: http://localhost:8000/docs
- 尝试各种功能
- 根据需求定制开发