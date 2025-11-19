# # backend/app/crud/crud_project.py - CORRECTED

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from ..models.project import Project
# from ..schemas.project import ProjectCreate

# async def create_project(db: AsyncSession, project: ProjectCreate, owner_id: int):
    
#     db_project = Project(**project.dict(), owner_id=owner_id)
#     db.add(db_project)
#     await db.commit()
#     await db.refresh(db_project)
#     return db_project

# async def get_projects_by_owner(db: AsyncSession, owner_id: int):
#     result = await db.execute(select(Project).filter(Project.owner_id == owner_id))
#     return result.scalars().all()

# backend/app/crud/crud_project.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.project import Project
from ..schemas.project import ProjectCreate
import json

async def create_project(db: AsyncSession, project: ProjectCreate, owner_id: int):

    # If sections exist, convert list → JSON string
    project_data = project.dict()
    if "sections" in project_data and project_data["sections"] is not None:
        project_data["sections"] = json.dumps(project_data["sections"])

    db_project = Project(**project_data, owner_id=owner_id)
    
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    
    return db_project


async def get_projects_by_owner(db: AsyncSession, owner_id: int):
    result = await db.execute(
        select(Project).filter(Project.owner_id == owner_id)
    )
    projects = result.scalars().all()

    # Convert JSON → list when sending response
    for p in projects:
        if p.sections:
            p.sections = json.loads(p.sections)

    return projects
