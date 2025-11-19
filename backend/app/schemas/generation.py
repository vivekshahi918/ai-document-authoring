# backend/app/schemas/generation.py

from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime


# This defines the input for the generation request
class GenerateRequest(BaseModel):
    main_topic: str
    section_titles: List[str]

# NEW SCHEMA just for getting the topic
class TopicRequest(BaseModel):
    main_topic: str

# This defines the output for a single generated section
class DocumentSection(BaseModel):
    id: int
    title: str
    content: str
    section_order: int
    project_id: int
    comment: Optional[str] = None # New
    feedback: Optional[str] = None # New

    class Config:
        orm_mode = True
        
class RefineRequest(BaseModel):
    prompt: str        
    
class SectionUpdate(BaseModel):
    comment: Optional[str] = None
    feedback: Optional[str] = None

class RefinementHistoryOut(BaseModel):
    id: int
    prompt: str
    created_at: datetime

    class Config:
        from_attributes = True   