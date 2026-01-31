from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any

Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    asset: Optional[str] = "BTC-USD"
    horizon: Optional[int] = 7

class ChatResponse(BaseModel):
    reply: str
    tool_calls: Optional[List[Dict[str, Any]]] = None