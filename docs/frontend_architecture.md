# Frontend Subsystem Architecture

This document describes the design, folder structure, design system, custom hooks, and technical architecture of the **Frontend User Interface Subsystem** (Phase 9) in the **ABTalks AI Interview Agent**.

---

## 🏗️ Folder Structure

The frontend adopts a **Feature-Based Architecture**:

```
frontend/src/
├── animations/                       # Centralized Framer Motion variants (fade, slide, scale, pageTransition)
├── assets/                           # Static assets, SVG icons, background graphics
├── components/
│   ├── charts/                       # ScoreChart, CategoryChart, CurriculumCoverageChart, ProgressTimeline
│   ├── common/                       # Toast, Skeleton, LoadingSpinner, EmptyState, ErrorState, ConfirmationDialog, ErrorBoundary
│   ├── layout/                       # Navbar, Sidebar, MobileNav, Footer
│   ├── results/                      # ScoreCard, FeedbackCard, RecommendationCard, KnowledgeGapCard
│   ├── session/                      # QuestionCard, AnswerEditor, ProgressTracker, Timer, TopicBadge, DifficultyBadge
│   └── ui/                           # Button, Input, Textarea, Select, Card, Modal, Dialog, Badge, Tooltip, Alert, Progress, Tabs, Accordion, Avatar, Skeleton, Divider
│
├── config/                           # API client, env variables, theme tokens
├── context/                          # InterviewContext, ThemeContext
├── features/
│   ├── dashboard/                    # DashboardPage
│   ├── history/                      # HistoryPage
│   ├── home/                         # HomePage
│   ├── interview/                    # LobbyPage, SessionPage
│   └── results/                      # ResultPage
│
├── hooks/                            # useInterview, useTimer, useProgress, useSession, useApi, useTheme, useToast, useLocalStorage
├── layouts/                          # MainLayout, DashboardLayout, InterviewLayout, ResultLayout, AuthLayout
├── pages/                            # Legacy page wrappers for feature components
├── services/                         # interview.js, results.js, session.js API clients
└── styles/                           # index.css (Tailwind & Glassmorphism Design System)
```

---

## 🎨 Theme Manager

- Supports **Light**, **Dark**, and **System Preference** theme modes via `ThemeContext` (`src/context/ThemeContext.jsx`) and `useTheme()` hook (`src/hooks/useTheme.js`).
- Persists user preferences seamlessly in `localStorage`.

---

## ⚡ Performance Optimization & Code Splitting

- **React.lazy() & Suspense**: Pages are dynamically imported on demand, reducing initial bundle size.
- **Memoization & Clean Hooks**: Decoupled state hooks (`useTimer`, `useProgress`, `useSession`, `useApi`) isolate rendering triggers.

---

## 🔮 Future Extensibility

The architecture is prepared for future enterprise expansions:
- **Authentication**: `AuthLayout` placeholder ready for OAuth2 / JWT integration.
- **Admin Dashboard & Analytics**: Feature modules can be added in `src/features/admin/`.
- **Multi-language Support (i18n)**: UI components consume string props cleanly.
