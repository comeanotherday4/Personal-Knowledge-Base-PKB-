# 项目开发指南

## 开发环境设置

### IDE推荐
- **VSCode**: 推荐安装Python、React、Docker插件
- **PyCharm**: 适合Python后端开发
- **WebStorm**: 适合前端开发

### VSCode推荐插件
- Python
- Pylance
- React Native Tools
- Docker
- ESLint
- Prettier

## 代码规范

### Python代码规范
- 使用PEP 8规范
- 函数和类添加文档字符串
- 类型注解（使用typing模块）
- 单元测试（pytest）

### JavaScript代码规范
- 使用ESLint和Prettier
- 函数式组件（React Hooks）
- 清晰的组件命名

## 测试

### 后端测试
```bash
# 安装测试依赖
pip install pytest pytest-asyncio httpx

# 运行测试
pytest tests/

# 测试覆盖率
pytest --cov=app tests/
```

### 前端测试
```bash
# 安装测试依赖
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# 运行测试
npm test
```

## 数据库迁移

### 使用Alembic
```bash
# 初始化Alembic
alembic init migrations

# 创建迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回退迁移
alembic downgrade -1
```

## API扩展

### 添加新的API端点
1. 在 `backend/app/api/` 创建新的路由文件
2. 在 `backend/app/services/` 实现业务逻辑
3. 在 `backend/main.py` 注册路由
4. 更新前端API服务

### 示例：添加用户管理API
```python
# backend/app/api/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    # 实现逻辑
    pass
```

## 前端组件开发

### 添加新页面
1. 在 `frontend/src/pages/` 创建组件
2. 在 `frontend/src/App.jsx` 添加路由
3. 在导航栏添加链接

### 添加新组件
1. 在 `frontend/src/components/` 创建组件
2. 在需要的页面中导入使用

## 性能优化

### 后端优化
- 使用异步处理（async/await）
- 数据库查询优化（索引、缓存）
- 文件处理异步化
- 使用Redis缓存频繁查询

### 前端优化
- 组件懒加载
- 图片优化
- API请求缓存
- 虚拟滚动（大列表）

## 安全考虑

### 后端安全
- 输入验证（Pydantic）
- 文件类型检查
- 文件大小限制
- SQL注入防护（ORM）
- API认证（JWT）

### 前端安全
- XSS防护
- CSRF防护
- 安全的API调用

## 部署建议

### 生产环境配置
- 使用环境变量管理配置
- 启用HTTPS
- 配置CORS策略
- 使用生产级数据库
- 启用日志记录
- 配置监控和告警

### Docker生产部署
```bash
# 使用生产配置
docker-compose -f docker-compose.prod.yml up -d

# 数据备份
docker-compose exec postgres pg_dump -U postgres knowledge_base > backup.sql
```

## 监控和日志

### 后端日志
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Document uploaded: %s", document.filename)
```

### 前端错误追踪
```javascript
// 使用try-catch处理错误
try {
  await api.uploadDocument(formData)
} catch (error) {
  console.error('Upload failed:', error)
  toast.error('上传失败')
}
```

## 功能扩展建议

### 短期扩展
1. 知识图谱可视化（D3.js或ECharts）
2. 文档编辑功能
3. 多用户支持
4. 知识导出（PDF、Word）

### 中期扩展
1. 移动端应用
2. 知识协作共享
3. AI模型微调
4. 知识质量评估

### 长期扩展
1. 企业版功能
2. 知识市场
3. AI Agent集成
4. 多语言支持

## 常见开发问题

### 问题1: 模块导入错误
```python
# 确保正确的导入路径
from app.models.database import Document  # 正确
from models.database import Document      # 错误
```

### 问题2: 数据库连接池
```python
# 使用连接池
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```

### 问题3: 前端状态管理
```javascript
// 使用React Hooks管理状态
const [documents, setDocuments] = useState([])
const [loading, setLoading] = useState(false)
```

## 调试技巧

### 后端调试
```python
# 使用print或logger调试
print(f"Processing document: {document.id}")
logger.debug("API called with params: %s", params)

# 使用FastAPI调试模式
uvicorn main:app --reload --debug
```

### 前端调试
```javascript
// 使用console.log调试
console.log('Documents:', documents)

// 使用React DevTools
// 安装Chrome扩展: React Developer Tools
```

## 版本控制

### Git工作流
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交代码
git add .
git commit -m "Add new feature"

# 合并到主分支
git checkout main
git merge feature/new-feature
```

### 提交信息规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关