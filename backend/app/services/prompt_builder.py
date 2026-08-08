import os
from typing import List, Optional
from app.models.candidate import CandidateModel
from app.models.curriculum import TopicModel, DayModel
from app.utils.file_utils import ensure_file_exists
from app.core.logging_config import logger


class PromptBuilder:
    """
    Constructs structured system and user prompts by loading external prompt templates
    from disk at startup with versioning 'v1.0'.
    """

    VERSION = "v1.0"
    _system_template: Optional[str] = None
    _question_template: Optional[str] = None
    _context_template: Optional[str] = None

    @classmethod
    def _load_templates(cls) -> None:
        """
        Loads prompt templates from disk once during initialization.
        """
        if cls._system_template is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            prompts_dir = os.path.join(base_dir, "prompts")

            sys_path = os.path.join(prompts_dir, "system_prompt.txt")
            q_path = os.path.join(prompts_dir, "question_prompt.txt")
            ctx_path = os.path.join(prompts_dir, "interview_context.txt")

            with open(ensure_file_exists(sys_path), "r", encoding="utf-8") as f:
                cls._system_template = f.read()
            with open(ensure_file_exists(q_path), "r", encoding="utf-8") as f:
                cls._question_template = f.read()
            with open(ensure_file_exists(ctx_path), "r", encoding="utf-8") as f:
                cls._context_template = f.read()

            logger.info(f"Prompt Templates Loaded: Successfully loaded '{cls.VERSION}' templates from disk.")

    @classmethod
    def build_question_generation_prompt(
        cls,
        candidate: CandidateModel,
        topic: TopicModel,
        day: Optional[DayModel],
        difficulty: str = "Intermediate",
        asked_questions: Optional[List[str]] = None,
        session_id: str = "default_session",
    ) -> str:
        """
        Builds a structured prompt by rendering external prompt template files.
        """
        cls._load_templates()

        asked_list_str = "\n".join([f"- {q}" for q in (asked_questions or [])]) or "None yet"
        learning_objs_str = "\n".join([f"- {o}" for o in (day.learning_objectives if day else [])]) or "General objective"
        tools_str = ", ".join(day.tools_used) if day else "General tools"

        context_rendered = cls._context_template.format(
            session_id=session_id,
            current_question_index=len(asked_questions or []),
            asked_questions_list=asked_list_str,
        )

        prompt_rendered = cls._question_template.format(
            candidate_name=candidate.full_name,
            target_role=candidate.target_role,
            experience_level=candidate.experience_level,
            completed_days=candidate.progress.completed_days,
            skipped_topics=candidate.skipped_topics or "None",
            day_number=day.day_number if day else 1,
            day_title=day.title if day else "Foundations",
            topic_title=topic.title,
            topic_category=topic.category,
            difficulty=difficulty,
            tools_used=tools_str,
            learning_objectives=learning_objs_str,
            conversation_context=context_rendered,
        )

        full_prompt = f"{cls._system_template}\n\n{prompt_rendered}"
        logger.info(f"Prompt Created: Rendered '{cls.VERSION}' prompt for topic '{topic.title}'.")
        return full_prompt
