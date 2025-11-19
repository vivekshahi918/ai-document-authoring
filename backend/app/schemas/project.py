# # backend/app/schemas/project.py

# from pydantic import BaseModel

# # Properties required when creating a project
# class ProjectCreate(BaseModel):
#     title: str
#     document_type: str # 'docx' or 'pptx'

# # Properties to return to the client
# class Project(BaseModel):
#     id: int
#     title: str
#     document_type: str
#     owner_id: int

#     class Config:
#         orm_mode = True # To work with SQLAlchemy models

# backend/app/schemas/project.py

from pydantic import BaseModel
from typing import List, Optional

# Properties required when creating a project
class ProjectCreate(BaseModel):
    title: str
    document_type: str  # 'docx' or 'pptx'

    # Optional additional fields (used for outline & content generation)
    main_topic: Optional[str] = None
    tone: Optional[str] = None
    sections: Optional[List[str]] = None
    target_audience: Optional[str] = None


# Properties returned to client
class Project(BaseModel):
    id: int
    title: str
    document_type: str
    owner_id: int

    # Extra fields returned if they exist
    main_topic: Optional[str] = None
    tone: Optional[str] = None
    sections: Optional[List[str]] = None
    target_audience: Optional[str] = None

    class Config:
        from_attributes = True  # To work with SQLAlchemy models
