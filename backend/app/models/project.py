from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .user import Base
import json
from typing import List

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    document_type = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    main_topic = Column(Text, nullable=True)
    tone = Column(String, nullable=True)
    target_audience = Column(String, nullable=True)
    sections = Column(Text, nullable=True)
    

    owner = relationship("User")
    def set_sections(self, sections_list: List[str]):
        """Converts a Python list to a JSON string before saving."""
        self.sections = json.dumps(sections_list)

    def get_sections(self) -> List[str]:
        """Converts the JSON string from the DB back into a Python list."""
        if self.sections:
            try:
                return json.loads(self.sections)
            except (json.JSONDecodeError, TypeError):
                return []
        return []