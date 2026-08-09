# Developer Onboarding & Contribution Guide

Guide for developers onboarding to the **ABTalks AI Interview Agent** codebase.

---

## 🛠️ Local Environment Setup

### 1. Prerequisites
- **Node.js**: v20+ recommended
- **Python**: 3.12+

### 2. Frontend Development Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Backend Development Setup
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🧪 Running Automated Tests

- **Backend Pytest**: `cd backend && python -m pytest -v`
- **Frontend Vitest**: `cd frontend && npm run test`
- **Frontend Build**: `cd frontend && npm run build`

---

## ➕ Adding New Curriculum Topics
Curriculum data is stored in `backend/app/data/curriculum.json`. Topics follow the Pydantic `TopicModel` schema:
```json
{
  "id": "top_new_topic",
  "title": "New Tech Topic Title",
  "category": "Backend"
}
```
Updating the JSON file automatically reloads the cache on startup or call to `CurriculumService().refresh_cache()`.
