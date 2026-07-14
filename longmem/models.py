"""Pydantic request/response models for the HTTP API."""
from typing import Optional

from pydantic import BaseModel


class RememberReq(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    content: str
    mem_type: str = "fact"  # fact | dialogue | preference


class RecallReq(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    query: str
    top_k: Optional[int] = None
    threshold: Optional[float] = None
