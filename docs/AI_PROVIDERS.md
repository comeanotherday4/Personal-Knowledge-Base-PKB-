"""AI服务商配置指南

本系统支持多种国内AI服务商，以下是各服务商的配置说明。

## 支持的AI服务商

### 1. 硅基流动 (SiliconFlow) ⭐ 推荐
**特点**: 国内访问速度快，免费额度多，支持多种开源模型

**官网**: https://www.siliconflow.cn/

**申请步骤**:
1. 访问 https://www.siliconflow.cn/
2. 注册/登录账号
3. 进入控制台 -> API密钥 -> 创建新密钥
4. 复制API Key

**配置示例**:
```env
AI_PROVIDER=siliconflow
AI_MODEL=Qwen/Qwen2.5-7B-Instruct
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.siliconflow.cn/v1
```

**可用模型**:
- Qwen/Qwen2.5-7B-Instruct (推荐，免费额度多)
- deepseek-ai/DeepSeek-V2.5
- THUDM/glm-4-9b-chat
- 零一万物/yi-large

---

### 2. 智谱AI (Zhipu)
**特点**: 清华大学技术积累，中文理解能力强

**官网**: https://www.zhipuai.cn/

**申请步骤**:
1. 访问 https://open.bigmodel.cn/
2. 注册/登录
3. 控制台 -> API Keys -> 创建API Key
4. 复制API Key

**配置示例**:
```env
AI_PROVIDER=zhipu
AI_MODEL=glm-4-flash
OPENAI_API_KEY=xxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://open.bigmodel.cn/api/paas/v4
```

**可用模型**:
- glm-4-flash (推荐，免费额度多)
- glm-4 (性能更强)
- glm-3-turbo (更便宜)

---

### 3. 百度文心一言 (Baidu)
**特点**: 百度技术积累，国产大模型

**官网**: https://cloud.baidu.com/

**申请步骤**:
1. 访问 https://cloud.baidu.com/
2. 注册/登录百度账号
3. 进入文心一言API控制台
4. 创建应用，获取API Key和Secret Key
5. 使用Secret Key换取Access Token（需要服务端实现）

**配置示例**:
```env
AI_PROVIDER=baidu
AI_MODEL=ernie-3.5-8k
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://qianfan.baidubce.com/v2
```

**注意**: 百度需要额外配置Secret Key，建议使用SDK方式接入

---

### 4. 阿里云通义千问 (Alibaba)
**特点**: 阿里技术积累，支持长文本

**官网**: https://dashscope.console.aliyun.com/

**申请步骤**:
1. 访问 https://dashscope.console.aliyun.com/
2. 注册/登录阿里云账号
3. 开通DashScope服务
4. 创建API Key
5. 复制API Key

**配置示例**:
```env
AI_PROVIDER=aliyun
AI_MODEL=qwen-turbo
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://dashscope.aliyuncs.com/api/v1
```

**可用模型**:
- qwen-turbo (推荐，便宜快速)
- qwen-plus (性能更强)
- qwen-max (最强性能)

---

### 5. MiniMax
**特点**: Moonshot团队创办，价格实惠

**官网**: https://www.minimax.io/

**申请步骤**:
1. 访问 https://platform.minimax.chat/
2. 注册/登录
3. 获取API Key

**配置示例**:
```env
AI_PROVIDER=minimax
AI_MODEL=abab6-chat
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://api.minimax.chat/v1
```

---

### 6. OpenAI (国际版)
**特点**: 业界标杆，技术领先

**官网**: https://platform.openai.com/

**注意**: 国内访问可能需要代理

**配置示例**:
```env
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.openai.com/v1
```

---

## 快速开始配置

### 方式一：使用硅基流动（推荐）

1. 访问 https://www.siliconflow.cn/
2. 注册并登录
3. 创建API Key
4. 编辑 `backend/.env` 文件：

```env
AI_PROVIDER=siliconflow
AI_MODEL=Qwen/Qwen2.5-7B-Instruct
OPENAI_API_KEY=sk-your-real-api-key
OPENAI_API_BASE=https://api.siliconflow.cn/v1
```

5. 重启后端服务

### 方式二：使用智谱AI

1. 访问 https://open.bigmodel.cn/
2. 注册并登录
3. 创建API Key
4. 编辑 `backend/.env` 文件：

```env
AI_PROVIDER=zhipu
AI_MODEL=glm-4-flash
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://open.bigmodel.cn/api/paas/v4
```

5. 重启后端服务

---

## 免费额度对比

| 服务商 | 免费额度 | 推荐模型 | 特点 |
|--------|---------|---------|------|
| 硅基流动 | 2000万Tokens | Qwen2.5-7B | 速度快，模型多 |
| 智谱AI | 500万Tokens | glm-4-flash | 中文好，清华技术 |
| 阿里云 | 100万Tokens | qwen-turbo | 稳定，阿里生态 |
| 百度 | 较少 | ernie-3.5 | 百度技术积累 |
| MiniMax | 赠送Tokens | abab6 | 价格便宜 |

---

## 常见问题

### Q: 选择哪个服务商？
**A**: 推荐硅基流动，免费额度多，速度快，支持多种模型。

### Q: 如何切换服务商？
**A**: 修改 `.env` 文件中的 `AI_PROVIDER` 和 `AI_MODEL`，然后重启服务。

### Q: API调用失败怎么办？
1. 检查API Key是否正确
2. 检查API Key是否有效/未过期
3. 检查网络连接
4. 查看后端日志错误信息
5. 确认服务商服务是否正常

### Q: 如何查看API使用量？
**A**: 登录各服务商的控制台查看API调用统计。

### Q: 如何优化API调用成本？
1. 使用更小的模型（如glm-4-flash代替glm-4）
2. 减少输入文本长度
3. 使用流式输出（如果支持）
4. 开启缓存

### Q: 国内服务需要备案吗？
**A**: 一般个人使用不需要备案，但商业使用需要确认服务商要求。

---

## 测试AI连接

启动服务后，访问 API文档 http://localhost:8000/docs

测试步骤：
1. 打开 POST /api/ai/summarize/{document_id}
2. 上传一个文档
3. 点击 "Try it out"
4. 查看返回结果

如果成功，说明AI配置正确。

---

## 技术支持

- 硅基流动: https://www.siliconflow.cn/
- 智谱AI: https://www.zhipuai.cn/
- 阿里云: https://help.aliyun.com/
- 百度云: https://cloud.baidu.com/
- MiniMax: https://platform.minimax.chat/

---

## 下一步

1. 选择一个服务商并申请API Key
2. 配置 `.env` 文件
3. 重启服务
4. 测试AI功能
5. 开始使用知识库系统