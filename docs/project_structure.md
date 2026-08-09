# Project Structure Map

Detailed map of the repository directory layout and module responsibilities.

```
abtalks/
├── frontend/                     # React 19 Frontend Application
│   ├── e2e/                      # End-to-End Test Specs
│   ├── src/
│   │   ├── components/           # UI Components & Error Boundaries
│   │   ├── config/               # API & Environment Configuration
│   │   ├── context/              # Context Providers (App, Theme, Interview, Loading)
│   │   ├── features/             # Page Feature Views (Home, Dashboard, Interview, Results, History)
│   │   ├── hooks/                # Custom Hooks (useNetworkStatus, etc.)
│   │   ├── services/             # Axios apiClient & Session Recovery Services
│   │   └── styles/               # Index CSS & Tailwind Styling
│   ├── tests/                    # Frontend Vitest Unit & Integration Tests
│   ├── vercel.json               # Vercel Deployment Configuration
│   └── vite.config.js            # Vite Bundler & Vitest Configuration
│
├── backend/                      # Python FastAPI Engine
│   ├── app/
│   │   ├── api/v1/               # Versioned REST Routers
│   │   ├── core/                 # Config, Cache, Logging & Security Middleware
│   │   ├── data/                 # JSON Datasets (curriculum, candidate, score_weights)
│   │   ├── memory/               # Session Memory Repository & Security
│   │   ├── models/               # Pydantic Data Models
│   │   ├── monitoring/           # Observability Metrics & Health Diagnostics
│   │   ├── providers/            # LLM Provider Interfaces & Mock Implementation
│   │   ├── services/             # Interview, Evaluation, & Feedback Engines
│   │   └── utils/                # Benchmark, Security Audit & Helper Utilities
│   ├── tests/                    # Backend Pytest Test Suites
│   ├── render.yaml               # Render Deployment Configuration
│   └── Procfile                  # Railway / Heroku Start Script
│
├── docs/                         # Technical Architecture & QA Documentation
├── .github/workflows/ci.yml      # Automated GitHub Actions CI Pipeline
├── ai-usage-log.md               # Hackathon AI Assistance Log
└── README.md                     # Root Project Guide
```
