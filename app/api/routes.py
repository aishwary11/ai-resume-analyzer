from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import ResumeAnalysis
from app.schemas.resume import AnalysisOut
from app.services.analysis import analyze_and_save
from app.services.pdf import extract_pdf_text

router = APIRouter(prefix="/api/v1/resumes", tags=["resume-analyzer"])


@router.post("/analyze", response_model=AnalysisOut)
async def analyze_resume(
    resume: Annotated[UploadFile, File()],
    job_description: Annotated[
        str,
        Form(
            ...,
            min_length=1,
            max_length=20000,
            description="Job title, position description, or analysis query.",
        ),
    ],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ResumeAnalysis:
    filename, resume_text = await extract_pdf_text(resume)
    return await analyze_and_save(db, filename, resume_text, job_description)


@router.get("/analyses", response_model=list[AnalysisOut])
async def list_analyses(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ResumeAnalysis]:
    result = await db.execute(
        select(ResumeAnalysis).order_by(ResumeAnalysis.created_at.desc()).limit(100)
    )
    return list(result.scalars().all())


@router.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisOut,
    responses={404: {"description": "Analysis not found"}},
)
async def get_analysis(
    analysis_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ResumeAnalysis:
    result = await db.execute(
        select(ResumeAnalysis).where(ResumeAnalysis.id == analysis_id)
    )
    record = result.scalar_one_or_none()
    if record is None:
        raise HTTPException(404, "Analysis not found")
    return record
