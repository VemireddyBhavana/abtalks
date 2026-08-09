# API Endpoint Reference

Complete documentation of all REST API endpoints provided by the **ABTalks AI Interview Agent** FastAPI backend.

---

## 📌 Base URL
`/api/v1`

---

## 🩺 Health & Diagnostics

### `GET /`
- **Summary**: Root Health Diagnostics
- **Response**: `{"status": "running", "project": "...", "curriculumLoaded": true, "candidateLoaded": true}`

### `GET /api/v1/health`
- **Summary**: Dedicated V1 Health Check
- **Response**: `{"status": "running", "curriculumLoaded": true, "candidateLoaded": true, "cacheReady": true}`

---

## 📚 Curriculum Intelligence

### `GET /api/v1/curriculum`
- **Summary**: Retrieves full curriculum tree model (5 days, topics, objectives, tools).

### `GET /api/v1/curriculum/search?keyword={kw}`
- **Summary**: Searches curriculum topics matching keyword.

### `GET /api/v1/curriculum/day/{day_number}`
- **Summary**: Retrieves specific day curriculum model.

---

## 👤 Candidate Intelligence

### `GET /api/v1/candidate`
- **Summary**: Retrieves candidate profile and progress metrics.

### `GET /api/v1/candidate/analytics`
- **Summary**: Retrieves completion rate, strongest topics, and weakest topics.

---

## 🎙️ Interview Engine

### `POST /api/v1/interview/start`
- **Body**: `{"candidate_id": "cand_alex_dev_99"}`
- **Response**: Returns session ID, question 1, and plan metadata.

### `POST /api/v1/interview/answer`
- **Body**: `{"session_id": "session_...", "answer_text": "Candidate response text..."}`
- **Response**: Processes turn, advances index, and returns next question or final feedback report when done.

### `GET /api/v1/interview/{session_id}`
- **Summary**: Retrieves full active session state model.

### `GET /api/v1/interview/{session_id}/summary`
- **Summary**: Retrieves session summary and completed report.
