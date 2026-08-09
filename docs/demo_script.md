# Hackathon Presentation & Live Demo Script

Presentation script for demonstrating the **ABTalks AI Interview Agent** during judging evaluation.

---

## 🎙️ Demo Presentation Plan (5 Minutes)

### 1. Introduction (0:00 - 0:45)
- **Speaker**: "Welcome! Today we present the ABTalks AI Interview Agent — a production-ready, full-stack platform designed to conduct dynamic technical interviews, evaluate responses across standard rubrics, and deliver actionable candidate scorecards."

### 2. Candidate Dashboard & Curriculum (0:45 - 1:30)
- Show candidate profile page (`/dashboard`), highlighting target role ("AI Engineer"), completion rate, curriculum progress (5 days), and learning signals.

### 3. Live Interview Execution (1:30 - 3:00)
- Navigate to `/lobby` and launch a session.
- Present **Question 1** (generated based on curriculum day topics).
- Enter candidate technical answer and submit.
- Show question progression and toast notifications.

### 4. Detailed Scorecard & Recommendations (3:00 - 4:15)
- Display the completed feedback report (`/result`).
- Highlight weighted category breakdown (Technical Accuracy, Concept Coverage, Terminology, Reasoning, Examples, Completeness, Communication).
- Show prioritized recommendations mapped to curriculum learning objectives.

### 5. Architectural Highlights & Closing (4:15 - 5:00)
- Explain decoupled Architecture (FastAPI backend + React 19 frontend).
- Mention OWASP security headers, session recovery on refresh, and zero-breaking-change modular design.
