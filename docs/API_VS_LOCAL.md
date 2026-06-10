# 📚 AI API vs 本地模型 - 详细说明

## 🤔 什么是 API 和本地模型？

### 🔹 API 方式（推荐）
使用第三方服务商提供的 AI 服务，比如：
- 硅基流动（SiliconFlow）⭐
- 智谱 AI
- 阿里云通义千问
- OpenAI

### 🔹 本地模型方式
在自己的电脑上运行 AI 模型，比如：
- Ollama
- Llama
- Qwen

---

## 📊 对比分析

| 特性 | API 方式 | 本地模型方式 |
|------|---------|-------------|
| **部署难度** | 🟢 简单，只需配置 Key | 🟡 中等，需要安装配置 |
| **硬件要求** | 🟢 无特殊要求 | 🔴 要求高，需要好显卡 |
| **速度** | 🟢 快，由服务商加速 | 🟡 取决于你的电脑 |
| **费用** | 🟡 按使用量计费 | 🟢 免费 |
| **数据安全** | 🟡 数据发送到第三方 | 🟢 完全本地，安全 |
| **模型更新** | 🟢 自动更新 | 🟡 需要手动更新 |
| **隐私保护** | 🟡 取决于服务商 | 🟢 完全隐私 |

---

## 🚀 API 方式（推荐新手）

### ✅ 优势
1. **零配置** - 只需一个 API Key
2. **高性能** - 强大的服务器集群
3. **最新模型** - 总是使用最好的模型
4. **免费额度** - 很多服务商提供免费试用

### 📋 如何配置（已支持）

**1. 硅基流动（推荐）**
```bash
# 官网: https://siliconflow.cn
# 免费额度: 2000万 Tokens
# 推荐模型: Qwen/Qwen2.5-7B-Instruct
```

配置你的 `.env` 文件：
```env
AI_PROVIDER=siliconflow
AI_MODEL=Qwen/Qwen2.5-7B-Instruct
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.siliconflow.cn/v1
```

**2. 其他国内服务商**
- **智谱 AI**: https://open.bigmodel.cn
- **阿里云**: https://dashscope.console.aliyun.com
- **百度文心**: https://cloud.baidu.com

---

## 💻 本地模型方式（技术用户）

### ✅ 优势
1. **完全免费**
2. **数据隐私** - 所有内容都在本地
3. **离线可用** - 不需要网络
4. **无限制** - 没有调用次数限制

### 🔧 配置步骤（Ollama 示例）

**1. 安装 Ollama**
- 官网: https://ollama.com
- 下载 Windows 版本并安装

**2. 下载模型**
```powershell
# 打开命令行，运行
ollama pull qwen2.5:7b
```

**3. 运行模型**
```powershell
ollama run qwen2.5:7b
```

**4. 在代码中集成**
```python
# Ollama 提供 OpenAI 兼容的 API
import requests

response = requests.post("http://localhost:11434/api/chat", json={
    "model": "qwen2.5:7b",
    "messages": [{"role": "user", "content": "你好"}]
})
```

### 💡 硬件要求

| 模型大小 | 显存需求 | 运行速度 |
|---------|---------|---------|
| 7B      | 8GB+    | 🟢 快 |
| 13B     | 16GB+   | 🟡 中 |
| 70B     | 64GB+   | 🔴 慢 |

### 🎯 推荐方案

**如果你是**：
- 👉 **个人用户/学习** → 使用硅基流动 API（免费额度足够）
- 👉 **敏感数据/企业** → 使用本地模型
- 👉 **有显卡/技术用户** → 两者结合使用

---

## 🎯 快速开始（建议）

### 阶段1：使用硅基流动 API（当前）
✅ 你已经申请了账号  
✅ 我们已经配置好了  
🚀 直接开始使用！

### 阶段2：想试试本地模型？
等你熟悉系统后，如果有好的显卡，可以：
1. 安装 Ollama
2. 下载 qwen2.5:7b
3. 切换配置

---

## ⚙️ 配置说明（完整）

### 硅基流动配置（.env）
```env
# 必需
OPENAI_API_KEY=sk-your-siliconflow-key

# 可选（默认值已经设置）
AI_PROVIDER=siliconflow
AI_MODEL=Qwen/Qwen2.5-7B-Instruct
OPENAI_API_BASE=https://api.siliconflow.cn/v1
```

### 本地模型配置（可选）
```env
# 使用 Ollama
OPENAI_API_KEY=ollama
OPENAI_API_BASE=http://localhost:11434/v1
AI_MODEL=qwen2.5:7b
```

---

## 📈 费用参考

| 服务商 | 免费额度 | 超出后价格 |
|--------|---------|-----------|
| 硅基流动 | 2000万 Tokens | ¥0.0001/千Token |
| 智谱 AI | 500万 Tokens | ¥0.001/千Token |
| 阿里云 | 100万 Tokens | ¥0.0008/千Token |

**估算**：10万字 ≈ 7万 Tokens，免费额度可以用很久！

---

## 🎉 总结

### 今天就可以开始：
1. ✅ **用硅基流动 API**（免费、快速、简单）
2. ✅ **在系统中上传文档**
3. ✅ **体验 AI 搜索和生成**

### 后续可选：
1. 安装 Ollama 试试本地模型
2. 探索其他国内服务商
3. 根据需要切换方式

---

## ❓ 常见问题

**Q: 我的文档会被发送到第三方吗？**  
A: 是的。如果你使用 API，文档片段会被发送用于处理。如果有隐私要求，建议使用本地模型。

**Q: API 调用会花钱吗？**  
A: 有免费额度，一般个人使用足够了。超出后才需要付费。

**Q: 本地模型一定会慢吗？**  
A: 取决于你的显卡。有好显卡（RTX 3060 以上）的话，速度也很快的。

**Q: 可以两种方式同时用吗？**  
A: 可以！可以根据任务选择不同的方式。
