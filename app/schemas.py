from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
import re

class LeadCreate(BaseModel):
    name: str
    email: str
    mobile: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @field_validator("email")
    @classmethod
    def email_valid(cls, v):
        v = v.strip().lower()
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(pattern, v):
            raise ValueError("Invalid email address")
        return v

    @field_validator("mobile")
    @classmethod
    def mobile_valid(cls, v):
        v = v.strip()
        if not re.match(r'^[6-9]\d{9}$', v):
            raise ValueError("Invalid Indian mobile number (must be 10 digits starting with 6-9)")
        return v

class LeadResponse(BaseModel):
    success: bool
    lead_id: int
    name: str

class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    lead_id: Optional[int] = None

class ChatResponse(BaseModel):
    reply: str

class LeadRecord(BaseModel):
    id: int
    name: str
    email: str
    mobile: str
    created_at: str
