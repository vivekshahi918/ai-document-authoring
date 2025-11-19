# # backend/app/models/project.py

# from sqlalchemy import Column, Integer, String, ForeignKey, Text
# from sqlalchemy.orm import relationship
# from .user import Base # Re-use the Base from the user model

# class Project(Base):
#     __tablename__ = "projects"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True, nullable=False)
#     document_type = Column(String, nullable=False) # Will be 'docx' or 'pptx'
#     owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     # This creates the relationship so we can easily access the owner
#     owner = relationship("User")

# backend/app/models/project.py

from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .user import Base
import json

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    document_type = Column(String, nullable=False)   # 'docx' or 'pptx'
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # New optional fields
    main_topic = Column(String, nullable=True)
    tone = Column(String, nullable=True)
    target_audience = Column(String, nullable=True)

    # Store list of sections as JSON text
    sections = Column(Text, nullable=True)

    owner = relationship("User")

    # Helper methods to convert sections JSON <-> list
    def set_sections(self, sections_list):
        self.sections = json.dumps(sections_list)

    def get_sections(self):
        if self.sections:
            return json.loads(self.sections)
        return []
