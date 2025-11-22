
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from .... import schemas
from ....db import AsyncSessionLocal
from .auth import get_current_user
from ....models.user import User as UserModel
from ....models.document_section import DocumentSection
from ....models.refinement_history import RefinementHistory 
from ....services import llm_service

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/{section_id}/refine", response_model=schemas.generation.DocumentSection)
async def refine_section_content(
    section_id: int,
    request: schemas.generation.RefineRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(select(DocumentSection).where(DocumentSection.id == section_id))
    db_section = result.scalars().first()

    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")
    

    history_entry = RefinementHistory(
        prompt=request.prompt,
        previous_content=db_section.content,
        section_id=section_id
    )
    db.add(history_entry)

    refined_content = await llm_service.refine_content_for_section(
        original_content=db_section.content,
        refinement_prompt=request.prompt
    )
    
    db_section.content = refined_content
    await db.commit() 
    await db.refresh(db_section)
    
    return db_section

@router.patch("/{section_id}", response_model=schemas.generation.DocumentSection)
async def update_section_details(
    section_id: int,
    section_update: schemas.generation.SectionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(select(DocumentSection).where(DocumentSection.id == section_id))
    db_section = result.scalars().first()

    if not db_section:
        raise HTTPException(status_code=404, detail="Section not found")

    if section_update.user_notes is not None:
        db_section.comment = section_update.user_notes
    
    if section_update.comment is not None:
        db_section.comment = section_update.comment

    if section_update.feedback is not None:
        db_section.feedback = section_update.feedback
        
    await db.commit()
    await db.refresh(db_section)
    return db_section


@router.get("/{section_id}/history", response_model=List[schemas.generation.RefinementHistoryOut])
async def get_section_refinement_history(
    section_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    result = await db.execute(
        select(RefinementHistory)
        .where(RefinementHistory.section_id == section_id)
        .order_by(RefinementHistory.created_at.desc()) 
    )
    history = result.scalars().all()
    return history