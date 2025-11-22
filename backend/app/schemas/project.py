

from pydantic import BaseModel
from typing import List, Optional

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
    sections: Optional[List[str]] = None
    target_audience: Optional[str] = None

    class Config:
        from_attributes = True  
