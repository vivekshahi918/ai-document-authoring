
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .user import Base

class RefinementHistory(Base):
    __tablename__ = "refinement_history"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    previous_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    section_id = Column(Integer, ForeignKey("document_sections.id"), nullable=False)

    section = relationship("DocumentSection")