import hashlib
import json
import logging

from redis.asyncio import Redis

from app.core.config import settings

logger = logging.getLogger(__name__)
redis_client = Redis.from_url(settings.redis_url, decode_responses=True)


def cache_key(resume_text: str, job_description: str) -> str:
    payload = {
        "prompt_version": "resume-analysis-v2",
        "base_url": settings.nvidia_base_url,
        "model": settings.nvidia_model,
        "resume": resume_text,
        "job_description": job_description,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    return "resume-analysis:" + digest


async def get_cached(key: str):
    try:
        value = await redis_client.get(key)
        return json.loads(value) if value else None
    except Exception:
        logger.exception("Redis read failed; bypassing cache")
        return None


async def set_cached(key: str, value: dict):
    try:
        await redis_client.set(
            key, json.dumps(value, ensure_ascii=False), ex=settings.redis_ttl_seconds
        )
    except Exception:
        logger.exception("Redis write failed; bypassing cache")


async def close_redis():
    await redis_client.aclose()
