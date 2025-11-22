
from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    main_topic: str
    section_titles: List[str]

class TopicRequest(BaseModel):
    main_topic: str

class DocumentSection(BaseModel):
    id: int
    title: str
    content: str
    section_order: int
    project_id: int
    comment: Optional[str] = None 
    feedback: Optional[str] = None 

    class Config:
        orm_mode = True
        
class RefineRequest(BaseModel):
    prompt: str        
    
class SectionUpdate(BaseModel):
    comment: Optional[str] = None
    user_notes: Optional[str] = None
    feedback: Optional[str] = None

class RefinementHistoryOut(BaseModel):
    id: int
    prompt: str
    created_at: datetime

    class Config:
        from_attributes = True   