from typing import List, Optional, Dict
from app.models.interview_engine import QuestionPlaceholderModel


class QuestionBank:
    """
    Static Question Bank repository of placeholder interview questions.
    Later in Phase 5, this static repository will be augmented/replaced by dynamic AI generation.
    """

    _QUESTIONS: List[QuestionPlaceholderModel] = [
        # Day 1 Questions
        QuestionPlaceholderModel(
            id="q_day1_react",
            day_number=1,
            topic_id="top_react_19",
            topic_title="React 19 & Client Routing",
            question_text="How do React 19 Server Components and React Router v7 optimize client-side bundle performance and route transitions?",
            difficulty="Intermediate"
        ),
        QuestionPlaceholderModel(
            id="q_day1_fastapi",
            day_number=1,
            topic_id="top_fastapi_core",
            topic_title="FastAPI ASGI & OpenAPI Specs",
            question_text="Explain the concurrency advantages of FastAPI's ASGI event loop over traditional WSGI frameworks like Flask.",
            difficulty="Fundamental"
        ),
        # Day 2 Questions
        QuestionPlaceholderModel(
            id="q_day2_axios",
            day_number=2,
            topic_id="top_axios_interceptors",
            topic_title="Axios Request/Response Interceptors",
            question_text="How do you implement global error handling and bearer token insertion using Axios interceptors in a modern React application?",
            difficulty="Intermediate"
        ),
        QuestionPlaceholderModel(
            id="q_day2_pydantic",
            day_number=2,
            topic_id="top_pydantic_settings",
            topic_title="Centralized Settings & Environment Parsing",
            question_text="Describe how pydantic-settings handles environment variable parsing, type validation, and fallback defaults in Python backend applications.",
            difficulty="Fundamental"
        ),
        # Day 3 Questions
        QuestionPlaceholderModel(
            id="q_day3_prompts",
            day_number=3,
            topic_id="top_system_prompts",
            topic_title="Interviewer Persona & Rubric System Prompts",
            question_text="What strategies ensure that AI system prompts adhere strictly to evaluation rubrics without hallucinating candidate scores?",
            difficulty="Advanced"
        ),
        QuestionPlaceholderModel(
            id="q_day3_memory",
            day_number=3,
            topic_id="top_context_memory",
            topic_title="In-Memory Buffer & Sliding Window Context",
            question_text="How does a sliding-window context memory buffer prevent LLM context limit truncation during multi-turn interviews?",
            difficulty="Intermediate"
        ),
        # Day 4 Questions
        QuestionPlaceholderModel(
            id="q_day4_mcp",
            day_number=4,
            topic_id="top_mcp_tools",
            topic_title="Model Context Protocol (MCP) Integration",
            question_text="Explain the architecture of Model Context Protocol (MCP) and how it enables AI agents to dynamically invoke external APIs.",
            difficulty="Advanced"
        ),
        QuestionPlaceholderModel(
            id="q_day4_agents",
            day_number=4,
            topic_id="top_agent_loops",
            topic_title="ReAct Agent Loops & Tool Execution",
            question_text="Describe the ReAct (Reasoning + Acting) loop pattern and how error recovery is managed when an agent tool call fails.",
            difficulty="Advanced"
        ),
        # Day 5 Questions
        QuestionPlaceholderModel(
            id="q_day5_rag",
            day_number=5,
            topic_id="top_rag_embeddings",
            topic_title="RAG Systems & Vector Search",
            question_text="How do vector embeddings, chunking strategies, and cosine similarity queries power Retrieval Augmented Generation (RAG)?",
            difficulty="Advanced"
        ),
        QuestionPlaceholderModel(
            id="q_day5_deploy",
            day_number=5,
            topic_id="top_cloud_deployment",
            topic_title="Containerized Cloud Deployment",
            question_text="What steps are required to containerize a FastAPI + Vite full-stack application and deploy it cleanly to Render or Vercel?",
            difficulty="Intermediate"
        ),
    ]

    @classmethod
    def get_all_questions(cls) -> List[QuestionPlaceholderModel]:
        """Returns all questions in bank."""
        return cls._QUESTIONS

    @classmethod
    def get_question(cls, question_id: str) -> Optional[QuestionPlaceholderModel]:
        """Retrieves a specific question by question ID."""
        for q in cls._QUESTIONS:
            if q.id == question_id:
                return q
        return None

    @classmethod
    def get_questions_by_day(cls, day_number: int) -> List[QuestionPlaceholderModel]:
        """Returns all questions covering a specific day."""
        return [q for q in cls._QUESTIONS if q.day_number == day_number]

    @classmethod
    def get_questions_by_topic(cls, topic_id: str) -> List[QuestionPlaceholderModel]:
        """Returns all questions matching a specific topic ID."""
        return [q for q in cls._QUESTIONS if q.topic_id == topic_id]

    @classmethod
    def get_question_count(cls) -> int:
        """Returns total question count in bank."""
        return len(cls._QUESTIONS)
