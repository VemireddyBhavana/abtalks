from app.services.feedback_engine import FeedbackEngine
from app.services.interview_engine import InterviewEngine


def test_feedback_engine_generation():
    session_engine = InterviewEngine()
    session_engine.start_interview(candidate_id="cand_feedback_test", session_id="sess_feedback_test")
    session = session_engine.state_manager.get_session("sess_feedback_test")
    
    engine = FeedbackEngine()
    report = engine.generate_feedback_report(session)
    assert report is not None
    assert report.session_id == "sess_feedback_test"
    assert report.overall_score is not None
