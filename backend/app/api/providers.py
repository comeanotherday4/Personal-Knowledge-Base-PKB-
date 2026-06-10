"""API路由 - AI服务商信息"""
from fastapi import APIRouter
from app.services.ai_service import AIService

router = APIRouter(prefix="/providers", tags=["AI服务商"])


@router.get("")
def list_providers():
    """列出所有支持的AI服务商"""
    providers = AIService.list_providers()
    return {
        "providers": providers,
        "total": len(providers),
        "recommendation": "推荐使用硅基流动(siliconflow)，免费额度多，速度快"
    }


@router.get("/{provider}/models")
def get_provider_models(provider: str):
    """获取指定服务商的可用模型"""
    providers = AIService.list_providers()
    provider_info = next((p for p in providers if p["id"] == provider), None)
    
    if not provider_info:
        return {"error": f"不支持的服务商: {provider}"}
    
    return {
        "provider": provider,
        "name": provider_info["name"],
        "models": provider_info["models"],
        "default_model": provider_info["default_model"]
    }