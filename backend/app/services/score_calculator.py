import json
import os
from typing import Dict, Any, List, Optional
from app.models.feedback_report import OverallScoreModel, CategoryScoreModel
from app.utils.file_utils import ensure_file_exists
from app.core.logging_config import logger


class ScoreCalculator:
    """
    Calculates weighted category scores and overall interview score (0-100).
    Loads external weight configuration from 'backend/app/config/score_weights.json'.
    """

    _weights_config: Optional[Dict[str, float]] = None

    @classmethod
    def _load_weights(cls) -> Dict[str, float]:
        if cls._weights_config is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "config", "score_weights.json")
            with open(ensure_file_exists(config_path), "r", encoding="utf-8") as f:
                data = json.load(f)
                cls._weights_config = data.get("weights", {})
            logger.info(f"Score Weights Loaded: Successfully loaded external weights configuration from {config_path}.")
        return cls._weights_config

    @classmethod
    def calculate_overall_score(cls, turn_answers: List[Dict[str, Any]]) -> OverallScoreModel:
        """
        Computes category breakdown scores and overall weighted score (0-100).
        """
        weights = cls._load_weights()
        logger.info("Score Calculation Started: Computing category breakdown and weighted scores...")

        if not turn_answers:
            return OverallScoreModel(
                overall_score=0.0,
                grade="F",
                rating_label="Unevaluated",
                breakdown=[],
            )

        evals = [turn.get("evaluation", {}) for turn in turn_answers if turn.get("evaluation")]
        
        # Raw metric aggregates
        avg_score = sum(e.get("score", 70) for e in evals) / len(evals) if evals else 70.0
        avg_conf = sum(e.get("confidence_score", 70) for e in evals) / len(evals) if evals else 70.0
        
        rubrics = [e.get("rubric", {}) for e in evals if e.get("rubric")]
        tech_acc = sum(r.get("technical_accuracy", 75) for r in rubrics) / len(rubrics) if rubrics else 75.0
        concept_cov = sum(r.get("concept_coverage", 75) for r in rubrics) / len(rubrics) if rubrics else 75.0
        reasoning = sum(r.get("reasoning", 70) for r in rubrics) / len(rubrics) if rubrics else 70.0
        
        metrics_list = [e.get("metrics", {}) for e in evals if e.get("metrics")]
        comm_clarity = sum(m.get("communication_clarity", 80) for m in metrics_list) / len(metrics_list) if metrics_list else 80.0

        # Consistency metric (lower variance -> higher consistency)
        scores_list = [e.get("score", 70) for e in evals]
        variance = sum((s - avg_score) ** 2 for s in scores_list) / len(scores_list) if scores_list else 0.0
        consistency = max(40.0, 100.0 - (variance ** 0.5))

        # Difficulty handling metric
        diff_handling = min(100.0, avg_score + 5.0)

        categories = [
            ("Technical Accuracy", tech_acc, weights.get("technical_accuracy", 0.25)),
            ("Concept Coverage", concept_cov, weights.get("concept_coverage", 0.20)),
            ("Reasoning", reasoning, weights.get("reasoning", 0.15)),
            ("Communication", comm_clarity, weights.get("communication", 0.10)),
            ("Confidence", avg_conf, weights.get("confidence", 0.10)),
            ("Consistency", consistency, weights.get("consistency", 0.10)),
            ("Difficulty Handling", diff_handling, weights.get("difficulty_handling", 0.10)),
        ]

        breakdown: List[CategoryScoreModel] = []
        weighted_total = 0.0

        for cat_name, raw_val, w in categories:
            w_score = round(raw_val * w, 2)
            weighted_total += w_score
            breakdown.append(
                CategoryScoreModel(
                    category_name=cat_name,
                    score=round(raw_val, 2),
                    weight=w,
                    weighted_score=w_score,
                    evaluation_notes=f"Evaluated across {len(evals)} interview turns.",
                )
            )

        final_score = round(weighted_total, 2)

        # Grade & Rating Label mapping
        if final_score >= 90:
            grade, rating = "A+", "Exceptional"
        elif final_score >= 80:
            grade, rating = "A", "Strong"
        elif final_score >= 70:
            grade, rating = "B", "Proficient"
        elif final_score >= 60:
            grade, rating = "C", "Developing"
        else:
            grade, rating = "F", "Needs Revision"

        logger.info(f"Score calculation completed: Overall Score {final_score}/100 (Grade {grade}, '{rating}').")

        return OverallScoreModel(
            overall_score=final_score,
            grade=grade,
            rating_label=rating,
            breakdown=breakdown,
        )
