

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.project import Project
from ..schemas.project import ProjectCreate

async def create_project(db: AsyncSession, project: ProjectCreate, owner_id: int) -> Project:
    
    project_data = project.dict()
    
    sections_list = project_data.pop("sections", None)
    db_project = Project(**project_data, owner_id=owner_id)
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