# AI Resume Analyzer

FastAPI + PostgreSQL + Redis + NVIDIA NIM starter.

## Run
1. Copy `.env.example` to `.env` and set `NVIDIA_API_KEY` to an NVIDIA API key.
2. Start PostgreSQL and Redis locally, then configure `DATABASE_URL` and `REDIS_URL` in `.env`.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Run `python -m uvicorn app.main:app --reload`.
5. Open http://localhost:8000/docs

## Analyze
```bash
curl.exe -X POST http://localhost:8000/api/v1/resumes/analyze `
  -F "resume=@.\resume.pdf" `
  -F "job_description=Python engineer with FastAPI, PostgreSQL and Docker experience."
```

The `job_description` field accepts a job title, role description, position requirements,
or a specific analysis query alongside the PDF upload.

## Endpoints
- `POST /api/v1/resumes/analyze` — upload PDF and analyze against a job description
- `GET /api/v1/resumes/analyses` — list recent analyses
- `GET /api/v1/resumes/analyses/{id}` — get one analysis
- `GET /health` — health check

## Design
- PostgreSQL stores analysis records and extracted resume text.
- Redis caches identical analyses by resume text + job description + model + prompt version.
- PDF text extraction uses PyMuPDF.
- Resume analysis uses NVIDIA NIM's OpenAI-compatible API.
- Structured output is validated with Pydantic.
- Resume and job-description text are treated as untrusted data; embedded instructions are not followed.

## Important
This is a learning scaffold, not a production hiring system. Add authentication, tenant isolation, Alembic migrations, malware scanning, rate limits, encryption, retention/deletion controls, audit logs, evaluation and bias testing before real deployment. Never use the score as an automatic hiring/rejection decision. Missing evidence means "not evidenced in this resume", not proof the candidate lacks a skill. Human review is required.
