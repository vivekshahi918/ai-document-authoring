from pydantic import BaseModel, Field
from typing import List, Optional, Union 

class ProjectSection(BaseModel):
    id: Optional[int] = None
    title: str
    content: Optional[str] = None  
    section_order: Optional[int] = None
    user_notes: Optional[str] = Field(default=None, alias="comment")
    feedback: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class ProjectCreate(BaseModel):
    title: str
    document_type: str  
    main_topic: Optional[str] = None
    tone: Optional[str] = None
    sections: Optional[List[str]] = None
    target_audience: Optional[str] = None

class Project(BaseModel):
    id: int
    title: str
    document_type: str
    owner_id: int

    main_topic: Optional[str] = None
    tone: Optional[str] = None
    sections: Optional[Union[List[ProjectSection], List[str]]] = []
    
    target_audience: Optional[str] = None

    class Config:
        from_attributes = True