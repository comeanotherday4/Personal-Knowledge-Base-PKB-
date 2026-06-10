"""AI服务 - 支持多种AI服务商"""
from typing import List, Dict, Optional
import json
import requests

settings = None  # 延迟初始化


def get_ai_settings():
    """获取AI配置"""
    global settings
    if settings is None:
        from app.config import get_settings
        settings = get_settings()
    return settings


class AIService:
    """AI服务，支持多种服务商"""
    
    # 支持的AI服务商配置
    PROVIDERS = {
        "siliconflow": {
            "name": "硅基流动",
            "base_url": "https://api.siliconflow.cn/v1",
            "models": ["Qwen/Qwen2.5-7B-Instruct", "deepseek-ai/DeepSeek-V2.5"],
            "default_model": "Qwen/Qwen2.5-7B-Instruct",
            "api_type": "openai_compatible"
        },
        "zhipu": {
            "name": "智谱AI",
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "models": ["glm-4-flash", "glm-4", "glm-3-turbo"],
            "default_model": "glm-4-flash",
            "api_type": "zhipu"
        },
        "baidu": {
            "name": "百度文心一言",
            "base_url": "https://qianfan.baidubce.com/v2",
            "models": ["ernie-4.0-8k-latest", "ernie-3.5-8k"],
            "default_model": "ernie-3.5-8k",
            "api_type": "baidu"
        },
        "aliyun": {
            "name": "阿里云通义千问",
            "base_url": "https://dashscope.aliyuncs.com/api/v1",
            "models": ["qwen-turbo", "qwen-plus"],
            "default_model": "qwen-turbo",
            "api_type": "openai_compatible"
        },
        "minimax": {
            "name": "MiniMax",
            "base_url": "https://api.minimax.chat/v1",
            "models": ["abab6-chat"],
            "default_model": "abab6-chat",
            "api_type": "openai_compatible"
        },
        "openai": {
            "name": "OpenAI",
            "base_url": "https://api.openai.com/v1",
            "models": ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"],
            "default_model": "gpt-4o-mini",
            "api_type": "openai"
        }
    }
    
    def __init__(self, provider: str = None):
        self.settings = get_ai_settings()
        
        # 如果未指定provider，从配置中获取
        if provider is None:
            provider = self.settings.AI_PROVIDER if hasattr(self.settings, 'AI_PROVIDER') else "siliconflow"
        
        self.provider = provider
        self.provider_config = self.PROVIDERS.get(provider, self.PROVIDERS["siliconflow"])
        self.model = self.settings.AI_MODEL if hasattr(self.settings, 'AI_MODEL') and self.settings.AI_MODEL else self.provider_config["default_model"]
        self.api_key = self.settings.OPENAI_API_KEY
        self.base_url = self.settings.OPENAI_API_BASE
        
        # 根据provider调整base_url
        if provider != "openai" and "openai" not in self.base_url.lower():
            self.base_url = self.provider_config["base_url"]
        
    def _call_api(self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 1000, json_mode: bool = False) -> str:
        """调用AI API"""
        url = f"{self.base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # 某些provider不支持response_format
        if json_mode and self.provider not in ["baidu"]:
            data["response_format"] = {"type": "json_object"}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # 兼容不同provider的响应格式
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            elif "output" in result:
                return result["output"]
            elif "text" in result:
                return result["text"]
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            print(f"API调用失败: {e}")
            return ""
        except Exception as e:
            print(f"处理响应失败: {e}")
            return ""

    def extract_knowledge_points(self, content: str, max_points: int = 10) -> List[Dict]:
        """从文档中提取知识点"""
        prompt = f"""请从以下文档内容中提取关键知识点。要求：
1. 提取最重要的知识点，最多{max_points}个
2. 每个知识点包含：标题、内容、重要程度(1-5)
3. 识别知识点之间的关联关系
4. 以JSON格式返回

文档内容：
{content[:4000]}

请按以下JSON格式返回：
{{
    "knowledge_points": [
        {{
            "title": "知识点标题",
            "content": "知识点详细内容",
            "importance": 5,
            "connections": ["相关知识点标题"]
        }}
    ]
}}
"""

        try:
            response = self._call_api([
                {"role": "system", "content": "你是一个专业的知识管理助手，擅长从文档中提取和组织知识。"},
                {"role": "user", "content": prompt}
            ], temperature=0.3, max_tokens=1500, json_mode=True)
            
            if response:
                result = json.loads(response)
                return result.get("knowledge_points", [])
            return []
        except Exception as e:
            print(f"提取知识点失败: {e}")
            return []

    def generate_summary(self, content: str, max_length: int = 200) -> str:
        """生成文档摘要"""
        prompt = f"""请为以下文档生成一个简洁的摘要，字数控制在{max_length}字以内：

文档内容：
{content[:3000]}

摘要：
"""

        try:
            response = self._call_api([
                {"role": "system", "content": "你是一个专业的文档摘要助手。"},
                {"role": "user", "content": prompt}
            ], temperature=0.5, max_tokens=300)
            
            return response.strip() if response else ""
        except Exception as e:
            print(f"生成摘要失败: {e}")
            return ""

    def generate_content(
        self,
        topic: str,
        context: List[str],
        style: str = "professional",
        length: int = 500
    ) -> str:
        """基于知识库生成内容"""
        style_prompts = {
            "professional": "专业、严谨、逻辑清晰",
            "casual": "轻松、易懂、口语化",
            "academic": "学术、深入、引用详实"
        }
        
        context_text = "\n\n".join([f"参考资料{i+1}:\n{c}" for i, c in enumerate(context)])
        
        prompt = f"""请基于以下参考资料，围绕主题"{topic}"生成一篇{style_prompts.get(style, '专业')}的文章。

要求：
1. 字数约{length}字
2. 充分利用参考资料中的信息
3. 保持逻辑连贯、内容充实
4. 如果参考资料不足，可以适当扩展

参考资料：
{context_text}

文章：
"""

        try:
            response = self._call_api([
                {"role": "system", "content": "你是一个专业的内容创作助手，擅长基于已有知识生成高质量文章。"},
                {"role": "user", "content": prompt}
            ], temperature=0.7, max_tokens=1500)
            
            return response.strip() if response else ""
        except Exception as e:
            print(f"生成内容失败: {e}")
            return ""

    def suggest_tags(self, content: str, existing_tags: List[str] = None) -> List[str]:
        """智能推荐标签"""
        existing_tags_text = f"已有标签：{', '.join(existing_tags)}\n" if existing_tags else ""
        
        prompt = f"""请为以下文档内容推荐合适的标签。

{existing_tags_text}
文档内容：
{content[:2000]}

要求：
1. 推荐3-5个最合适的标签
2. 标签应简洁、准确
3. 优先使用已有标签，必要时创建新标签
4. 以JSON格式返回，格式：{{"tags": ["标签1", "标签2", "标签3"]}}

标签：
"""

        try:
            response = self._call_api([
                {"role": "system", "content": "你是一个文档分类专家。"},
                {"role": "user", "content": prompt}
            ], temperature=0.3, max_tokens=200, json_mode=True)
            
            if response:
                result = json.loads(response)
                return result.get("tags", result.get("labels", []))
            return []
        except Exception as e:
            print(f"推荐标签失败: {e}")
            return []

    def answer_question(self, question: str, context: List[Dict]) -> str:
        """基于知识库回答问题"""
        context_text = "\n\n".join([
            f"参考文档{i+1}（来源：{c.get('filename', '未知')}）:\n{c.get('content', '')}"
            for i, c in enumerate(context)
        ])
        
        prompt = f"""请基于以下参考资料回答问题。如果参考资料中没有相关信息，请明确说明。

参考资料：
{context_text}

问题：{question}

回答：
"""

        try:
            response = self._call_api([
                {"role": "system", "content": "你是一个知识渊博的助手，善于基于已有知识回答问题。"},
                {"role": "user", "content": prompt}
            ], temperature=0.5, max_tokens=800)
            
            return response.strip() if response else ""
        except Exception as e:
            print(f"回答问题失败: {e}")
            return ""

    def find_connections(self, knowledge_points: List[Dict]) -> List[Dict]:
        """发现知识点之间的关联"""
        points_text = "\n".join([
            f"{i+1}. {p['title']}: {p['content'][:100]}"
            for i, p in enumerate(knowledge_points)
        ])
        
        prompt = f"""请分析以下知识点之间的关联关系。

知识点：
{points_text}

要求：
1. 识别知识点之间的关联（如：因果关系、包含关系、对比关系等）
2. 以JSON格式返回关联关系
3. 格式：{{"connections": [{{"from": "知识点1", "to": "知识点2", "type": "关联类型", "strength": 1-5}}]}}

关联关系：
"""

        try:
            response = self._call_api([
                {"role": "system", "content": "你是一个知识图谱专家。"},
                {"role": "user", "content": prompt}
            ], temperature=0.3, max_tokens=1000, json_mode=True)
            
            if response:
                result = json.loads(response)
                return result.get("connections", [])
            return []
        except Exception as e:
            print(f"发现关联失败: {e}")
            return []

    @staticmethod
    def list_providers() -> List[Dict]:
        """列出支持的AI服务商"""
        return [
            {
                "id": key,
                "name": config["name"],
                "models": config["models"],
                "default_model": config["default_model"]
            }
            for key, config in AIService.PROVIDERS.items()
        ]