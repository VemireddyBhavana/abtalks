# 🎙️ AI Interview Agent - ABTalks AI Hackathon

A production-ready full-stack AI Interview Agent project foundation built for the **ABTalks AI Interview Agent Hackathon**.

---

## 📌 Project Overview

The **AI Interview Agent** is an interactive web platform designed to conduct AI-powered interviews, evaluate candidates, and deliver detailed feedback scorecards. 

This repository provides a modular, scalable, and production-ready foundation separated into a modern React 19 frontend powered by Vite & Tailwind CSS, and a Python FastAPI backend.

---

## 📁 Folder Structure

```
ai-interview-agent/
│
├── frontend/
│   ├── src/
│   │   ├── assets/        # Static assets (images, icons, svgs)
│   │   ├── components/    # Reusable UI components (Navbar, Header, Card, etc.)
│   │   ├── pages/         # Page views (Home, Interview, Result, NotFound)
│   │   ├── layouts/       # Main container & layout wrappers
│   │   ├── hooks/         # Custom React hooks (useApi, etc.)
│   │   ├── services/      # Axios API client setup and endpoints
│   │   ├── utils/         # Helper functions & global constants
│   │   ├── styles/        # Global CSS & Tailwind configuration
│   │   ├── App.jsx        # Root routing component
│   │   └── main.jsx       # Application entry point
│   │
│   ├── package.json       # Frontend dependencies & scripts
│   ├── vite.config.js     # Vite bundler configuration & proxy settings
│   ├── tailwind.config.js # Tailwind CSS theme tokens & utilities
│   ├── postcss.config.js  # PostCSS configuration
│   └── .env.example       # Environment variables template
│
├── backend/
│   ├── app/
│   │   ├── api/           # API routes & endpoint definitions
│   │   ├── models/        # Pydantic schemas & data models
│   │   ├── services/      # Business logic & service handlers
│   │   ├── utils/         # Helper utilities & loggers
│   │   ├── core/          # Core settings, CORS, and configs
│   │   ├── data/          # Static datasets or mock stores
│   │   └── main.py        # FastAPI server entry point
│   │
│   ├── requirements.txt   # Python dependencies
│   ├── .env.example       # Backend environment variables template
│   └── README.md          # Backend documentation
│
├── docs/                  # Architecture & API documentation
├── prompts/               # Prompt templates & evaluator rubrics
├── ai-usage-log.md        # AI usage and prompt engineering log
├── README.md              # Root project overview & guide
├── .gitignore             # Git ignore configuration
└── LICENSE                # Project license (MIT)
```

---

## 🚀 Getting Started & Installation

### Prerequisites
- **Node.js**: v18.x or later (v20+ recommended)
- **npm**: v9.x or later
- **Python**: 3.12 or later

---

### 1️⃣ Setting Up the Frontend

Navigate to the `frontend/` directory:
```bash
cd frontend
```

Install frontend dependencies:
```bash
npm install
```

Copy the environment file:
```bash
cp .env.example .env
```

Start the frontend development server:
```bash
npm run dev
```

The application will be running at `http://localhost:5173`.

---

### 2️⃣ Setting Up the Backend

Navigate to the `backend/` directory:
```bash
cd backend
```

Create a Python virtual environment:
```bash
# On Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# On Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:
```bash
pip install -r requirements.txt
```

Copy the environment file:
```bash
cp .env.example .env
```

Start the FastAPI backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Open `http://localhost:8000/docs` to view the interactive Swagger API documentation.

---

## 🔌 API Endpoints (Foundation)

| Method | Endpoint | Description | Expected Output |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Root Health Check | `{"status": "running", "project": "AI Interview Agent"}` |
| `GET` | `/health` | Dedicated Health Check | `{"status": "healthy", "service": "backend"}` |

---

## 🌐 Deployment Targets

- **Frontend**: Designed for deployment on **Vercel** (`vite build` -> output directory `frontend/dist`).
- **Backend**: Designed for deployment on **Render** or **Railway** (using Uvicorn web server).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
