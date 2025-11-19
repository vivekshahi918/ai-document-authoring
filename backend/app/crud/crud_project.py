# backend/app/crud/crud_project.py - FINAL VERSION

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.project import Project
from ..schemas.project import ProjectCreate

async def create_project(db: AsyncSession, project: ProjectCreate, owner_id: int) -> Project:
    
    # Convert the Pydantic schema to a dictionary
    project_data = project.dict()
    
    # Pop the 'sections' list because it needs special handling via the model's method
    sections_list = project_data.pop("sections", None)

    # Create the Project database object with the main data
    db_project = Project(**project_data, owner_id=owner_id)

    # If a sections list was provided, use the model's helper method to convert it to a JSON string
    if sections_list:
        db_project.set_sections(sections_list)

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    
    return db_project


async def get_projects_by_owner(db: AsyncSession, owner_id: int) -> list[Project]:

    result = await db.execute(
        select(Project).filter(Project.owner_id == owner_id).order_by(Project.id.desc())
    )
    return result.scalars().all()