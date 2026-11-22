from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceItem(BaseModel):
    criterion: str
    status: str = Field(description="met, partial, not_evidenced, or unclear")
    resume_evidence: str
    explanation: str


class ResumeAnalysisResult(BaseModel):
    candidate_summary: str
    role_summary: str
    overall_match_score: int = Field(ge=0, le=100)
    score_explanation: str
    matching_strengths: list[str]
    skill_gaps_or_unverified_requirements: list[str]
    evidence_by_criterion: list[EvidenceItem]
    relevant_experience: list[str]
    suggested_follow_up_questions: list[str]
    limitations: list[str]


class AnalysisOut(BaseModel):
    id: int
    filename: str
    model: str
    cache_hit: bool
    result: ResumeAnalysisResult
    created_at: datetime
    model_config = {"from_attributes": True}
