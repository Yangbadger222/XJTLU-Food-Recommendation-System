"""Chat API routes for AI conversation."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services import get_deepseek_service

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """聊天消息模型."""
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    """聊天响应模型."""
    response: str


@router.post("", response_model=ChatResponse)
async def chat_with_ai(chat: ChatMessage):
    """
    与AI营养师对话.
    
    可以询问关于饮食、营养、健康的任何问题。
    """
    try:
        service = get_deepseek_service()
        response = await service.chat(
            user_message=chat.message,
            conversation_history=chat.conversation_history
        )
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")
