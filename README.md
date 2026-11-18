# LLM-Powered Automated Code Review and Analysis System

An independently written, university-level FastAPI starter application for reviewing code with Google Gemini. Built with a simple browser UI, SQLite persistence, and API tests. **No code from a third-party GitHub project has been copied into this repository.**

## Working features
- `POST /api/reviews` accepts language and source code, then calls Gemini when a key is configured.
- Without a key, an explicitly labeled **offline demo mode** produces illustrative heuristic results; it is **not an LLM review**.
- `GET /api/reviews`, `GET /api/reviews/{id}` provide stored review history.
- `GET /health`, `GET /docs`, and `/` (browser frontend).
- SQLite persistence, request validation, and pytest tests.

## Quick start (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

## Quick start (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/ or http://127.0.0.1:8000/docs. Set your `GEMINI_API_KEY` in `.env` for actual model reviews. The model may be changed using `GEMINI_MODEL` if needed. An API key may incur charges.

## Test
```bash
pytest -q
```

## Docker
```bash
docker build -t llm-code-review .
docker run --rm -p 8000:8000 --env-file .env llm-code-review
```

## Architecture
Browser UI → FastAPI → Gemini generateContent API → SQLite review history.

## Limitations / possible improvements
- This **starter is not production-ready**: no authentication, multi-user isolation, sandboxed code execution, PostgreSQL, background queue or rate limiting yet.
- Do **not** send secrets or confidential source code to a third-party model.
- LLM reviews can be wrong. Review suggested changes and run your own tests.
- Suggested next steps: PostgreSQL + SQLAlchemy; JWT auth; structured Pydantic response validation; background jobs; GitHub PR integrations; Docker Compose.

## Authorship
Original starter implementation generated for customization and educational use. Document what you personally change before describing the work as your own resume project. If you later copy external source code, comply with its license terms.
