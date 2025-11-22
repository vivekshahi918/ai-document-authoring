
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .user import Base

class DocumentSection(Base):
    __tablename__ = "document_sections"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    section_order = Column(Integer, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    comment = Column(Text, nullable=True)
    feedback = Column(String, nullable=True)

    project = relationship("Project")
    
   
    history_entries = relationship("RefinementHistory", back_populates="section", cascade="all, delete-orphan")