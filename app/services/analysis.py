from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.entities import ResumeAnalysis
from app.services.cache import cache_key, get_cached, set_cached
from app.services.llm import analyze


async def analyze_and_save(
    db: AsyncSession, filename: str, resume_text: str, job_description: str
):
    key = cache_key(resume_text, job_description)
    result = await get_cached(key)
    cache_hit = result is not None
    model = settings.nvidia_model
    if not cache_hit:
        parsed = await analyze(resume_text, job_description)
        result = parsed.model_dump()
        await set_cached(key, result)
    record = ResumeAnalysis(
        filename=filename,
        job_description=job_description,
        resume_text=resume_text,
        result=result,
        model=model,
        cache_hit=cache_hit,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record
