import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import List

from .... import crud, schemas
from ....db import AsyncSessionLocal
from .auth import get_current_user
from ....models.user import User as UserModel
from ....models.project import Project 
from ....models.document_section import DocumentSection
from ....services import llm_service, document_service
from ....services.document_service import SectionData
from ....schemas.generation import GenerateRequest, DocumentSection as SectionSchema
from ....schemas.generation import TopicRequest
from ....schemas.project import ProjectSection 

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=schemas.Project, status_code=status.HTTP_201_CREATED)
async def create_new_project(
    project: schemas.ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    return await crud.create_project(db=db, project=project, owner_id=current_user.id)

@router.get("/", response_model=List[schemas.Project])
async def read_user_projects(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    projects_from_db = await crud.get_projects_by_owner(db=db, owner_id=current_user.id)
    
    response_projects = []
    for project in projects_from_db:
        project_schema = schemas.Project.from_orm(project)
        
        raw_sections = project.get_sections()
        if raw_sections and isinstance(raw_sections[0], str):
             project_schema.sections = raw_sections
        else:
             project_schema.sections = raw_sections

        response_projects.append(project_schema)
        
    return response_projects

@router.get("/{project_id}", response_model=schemas.Project)
async def read_project_details(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()

    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Project not found")

    sections_result = await db.execute(
        select(DocumentSection)
        .where(DocumentSection.project_id == project_id)
        .order_by(DocumentSection.section_order)
    )
    generated_sections = sections_result.scalars().all()

    project_schema = schemas.Project.from_orm(project)

    if generated_sections:
        project_schema.sections = [
            ProjectSection.model_validate(sec) for sec in generated_sections
        ]
    else:
        project_schema.sections = project.get_sections()
    
    return project_schema

@router.post("/{project_id}/generate", response_model=List[SectionSchema])
async def generate_document_content(
    project_id: int,
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.main_topic = request.main_topic
    db.add(project)
    
    await db.execute(
        delete(DocumentSection).where(DocumentSection.project_id == project_id)
    )
    
    await db.commit()
    
    generated_sections = []
    for i, section_title in enumerate(request.section_titles):
        content = await llm_service.generate_content_for_section(
            main_topic=request.main_topic,
            section_title=section_title
        )
        
        db_section = DocumentSection(
            title=section_title,
            content=content,
            section_order=i,
            project_id=project_id
        )
        db.add(db_section)
        generated_sections.append(db_section)

        await asyncio.sleep(1.5)
    await db.commit()

    for section in generated_sections:
        await db.refresh(section)
        
    return generated_sections

@router.get("/{project_id}/export")
async def export_project_document(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):

    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # TODO: Verify current_user owns this project

    sections_result = await db.execute(
        select(DocumentSection)
        .where(DocumentSection.project_id == project_id)
        .order_by(DocumentSection.section_order)
    )
    sections = sections_result.scalars().all()

    valid_sections = [
        s for s in sections if s.content and "Error: Could not generate content" not in s.content
    ]
    
    if not valid_sections:
        raise HTTPException(status_code=400, detail="No valid content to export.")
    
    section_data = [SectionData(title=s.title, content=s.content) for s in valid_sections]
    
    file_stream = None
    media_type = ""
    safe_title = "".join(c for c in project.title if c.isalnum() or c in (' ', '_')).rstrip()
    filename = f"{safe_title.replace(' ', '_')}.unknown"


    if project.document_type == 'docx':
        file_stream = document_service.create_word_document(section_data)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename = f"{safe_title}.docx"
    elif project.document_type == 'pptx':
        file_stream = document_service.create_powerpoint_presentation(section_data)
        media_type = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        filename = f"{safe_title}.pptx"
    else:
       
        raise HTTPException(status_code=400, detail="Unsupported document type")
    
    return StreamingResponse(
    file_stream,
    media_type=media_type,
    headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

        
@router.post("/{project_id}/suggest-outline", response_model=List[str])
async def suggest_document_outline(
    project_id: int,
    request: TopicRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    outline = await llm_service.generate_outline(request.main_topic, project.document_type)
    return outline