# Production Deployment Guide

This guide details step-by-step instructions for deploying the **ABTalks AI Interview Agent** to production environments on **Vercel** (Frontend) and **Render / Railway** (Backend).

---

## 🌐 1. Frontend Deployment (Vercel)

### Prerequisites
- Vercel CLI installed (`npm i -g vercel`) or connected GitHub account.

### Steps
1. Connect repository to Vercel via Dashboard or execute CLI in `frontend/`:
   ```bash
   cd frontend
   vercel
   ```
2. **Build Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. **Environment Variables**:
   - `VITE_API_BASE_URL`: `https://abtalks-api.onrender.com/api/v1`
4. Configuration is automatically applied via `frontend/vercel.json`.

---

## 🐍 2. Backend Deployment (Render / Railway)

### Deploying on Render
1. Create a **Web Service** connected to the GitHub repository.
2. Root directory: `backend`
3. **Environment**: Python 3.12+
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Configuration can be imported automatically via `backend/render.yaml`.

### Deploying on Railway
1. Connect repository to Railway.
2. Root directory: `backend`
3. Railway automatically detects `backend/Procfile` and launches Uvicorn.
