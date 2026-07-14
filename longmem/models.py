"""Pydantic request/response models for the HTTP API."""
from typing import List, Optional

from pydantic import BaseModel


class RememberReq(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    content: str
    mem_type: str = "fact"  # fact | dialogue | preference
    ttl_seconds: Optional[int] = None  # None = never expires


class RememberItem(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    content: str
    mem_type: str = "fact"
    ttl_seconds: Optional[int] = None


class BatchRememberReq(BaseModel):
    items: List[RememberItem]


class RecallReq(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    query: str
    top_k: Optional[int] = None
    threshold: Optional[float] = None
