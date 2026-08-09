# Full-Stack System Architecture

This document describes the high-level system architecture, design patterns, and subsystem interactions of the **ABTalks AI Interview Agent**.

---

## 🏗️ High-Level System Architecture

```mermaid
graph TD
    subgraph Client Layer
        React[React 19 SPA]
        Ctx[InterviewContext]
        Rec[sessionRecovery]
        Net[useNetworkStatus]
    end

    subgraph API Integration
        Axios[apiClient]
        Guard[RouteGuards & ApiErrorBoundary]
    end

    subgraph Backend Engine
        FastAPI[FastAPI Router]
        Engine[InterviewEngine]
        Feedback[FeedbackEngine]
        Memory[MemoryRepository]
        Cache[InMemoryCacheManager]
        LLM[LLMService & MockProvider]
    end

    React --> Ctx
    Ctx --> Rec
    Ctx --> Net
    Ctx --> Axios
    Axios --> FastAPI
    FastAPI --> Engine
    Engine --> Feedback
    Engine --> Memory
    Engine --> Cache
    Engine --> LLM
```

---

## 🧩 Architectural Design Patterns

1. **Strategy Pattern**:
   - Used in `InterviewEngine` (`StandardInterviewStrategy`, `FutureAdaptiveStrategy`) and `FeedbackEngine` (`TechnicalFeedbackStrategy`, `BehavioralFeedbackStrategy`).
2. **Factory Pattern**:
   - `InterviewFactory`, `MemoryFactory`, and `LLMProviderFactory` construct interface implementations cleanly.
3. **Singleton Pattern**:
   - `InMemoryCacheManager`, `MetricsRegistry`, and `PerformanceMonitor` maintain centralized state.
4. **Repository Pattern**:
   - `MemoryRepository` decouples storage providers from business logic.
