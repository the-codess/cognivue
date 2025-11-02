"""
Feedback Collector
Collects and stores user feedback
"""
import uuid
from typing import List, Optional, Dict
from datetime import datetime, timedelta

from src.modules.feedback_learning.models import (
    InsightFeedback, ReportFeedback, ImplicitFeedback,
    FeedbackType, FeedbackSummary
)
from src.utils.logger import app_logger as logger

class FeedbackCollector:
    """Collect and manage user feedback"""
    
    def __init__(self):
        self.insight_feedback: Dict[str, List[InsightFeedback]] = {}
        self.report_feedback: List[ReportFeedback] = []
        self.implicit_feedback: List[ImplicitFeedback] = []
        logger.info("FeedbackCollector initialized")
    
    def record_insight_feedback(
        self,
        insight_id: str,
        rating: Optional[int] = None,
        is_relevant: Optional[bool] = None,
        is_accurate: Optional[bool] = None,
        comment: Optional[str] = None,
        user_id: Optional[str] = None,
        role_id: Optional[str] = None
    ) -> InsightFeedback:
        """Record feedback on an insight"""
        
        feedback = InsightFeedback(
            feedback_id=f"fb_{uuid.uuid4().hex[:8]}",
            insight_id=insight_id,
            user_id=user_id,
            role_id=role_id,
            feedback_type=FeedbackType.RATING,
            rating=rating,
            is_relevant=is_relevant,
            is_accurate=is_accurate,
            comment=comment
        )
        
        # Store feedback
        if insight_id not in self.insight_feedback:
            self.insight_feedback[insight_id] = []
        self.insight_feedback[insight_id].append(feedback)
        
        logger.info(f"Recorded feedback for insight {insight_id}: rating={rating}")
        return feedback
    
    def record_report_feedback(
        self,
        report_id: str,
        overall_rating: int,
        relevance_rating: int,
        clarity_rating: int,
        actionability_rating: int,
        what_worked_well: Optional[str] = None,
        what_needs_improvement: Optional[str] = None,
        user_id: Optional[str] = None,
        role_id: Optional[str] = None
    ) -> ReportFeedback:
        """Record feedback on entire report"""
        
        feedback = ReportFeedback(
            feedback_id=f"fb_{uuid.uuid4().hex[:8]}",
            report_id=report_id,
            user_id=user_id,
            role_id=role_id,
            overall_rating=overall_rating,
            relevance_rating=relevance_rating,
            clarity_rating=clarity_rating,
            actionability_rating=actionability_rating,
            what_worked_well=what_worked_well,
            what_needs_improvement=what_needs_improvement
        )
        
        self.report_feedback.append(feedback)
        
        logger.info(f"Recorded report feedback: overall={overall_rating}/5")
        return feedback
    
    def record_implicit_feedback(
        self,
        insight_id: str,
        time_spent_viewing: float,
        clicked: bool = False,
        drilled_down: bool = False,
        shared: bool = False,
        user_id: Optional[str] = None
    ) -> ImplicitFeedback:
        """Record implicit feedback from user behavior"""
        
        feedback = ImplicitFeedback(
            feedback_id=f"fb_{uuid.uuid4().hex[:8]}",
            insight_id=insight_id,
            user_id=user_id,
            time_spent_viewing=time_spent_viewing,
            clicked=clicked,
            drilled_down=drilled_down,
            shared=shared
        )
        
        self.implicit_feedback.append(feedback)
        
        logger.debug(f"Recorded implicit feedback for {insight_id}")
        return feedback
    
    def get_insight_feedback(self, insight_id: str) -> List[InsightFeedback]:
        """Get all feedback for an insight"""
        return self.insight_feedback.get(insight_id, [])
    
    def get_average_rating(self, insight_id: str) -> Optional[float]:
        """Get average rating for an insight"""
        feedback_list = self.get_insight_feedback(insight_id)
        ratings = [f.rating for f in feedback_list if f.rating is not None]
        
        if not ratings:
            return None
        
        return sum(ratings) / len(ratings)
    
    def get_feedback_summary(
        self,
        days: int = 7
    ) -> FeedbackSummary:
        """Generate feedback summary for recent period"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Filter recent feedback
        recent_insight_feedback = []
        for feedback_list in self.insight_feedback.values():
            recent_insight_feedback.extend([
                f for f in feedback_list
                if f.timestamp >= start_date
            ])
        
        recent_report_feedback = [
            f for f in self.report_feedback
            if f.timestamp >= start_date
        ]
        
        # Calculate aggregates
        total_feedback = len(recent_insight_feedback) + len(recent_report_feedback)
        
        if total_feedback == 0:
            avg_rating = 0.0
            positive_rate = 0.0
            negative_rate = 0.0
        else:
            # Average rating from insights
            insight_ratings = [f.rating for f in recent_insight_feedback if f.rating]
            report_ratings = [f.overall_rating for f in recent_report_feedback]
            all_ratings = insight_ratings + report_ratings
            
            avg_rating = sum(all_ratings) / len(all_ratings) if all_ratings else 0.0
            positive_rate = sum(1 for r in all_ratings if r >= 4) / len(all_ratings) if all_ratings else 0.0
            negative_rate = sum(1 for r in all_ratings if r <= 2) / len(all_ratings) if all_ratings else 0.0
        
        # Collect common themes
        comments = [f.comment for f in recent_insight_feedback if f.comment]
        improvements = [f.what_needs_improvement for f in recent_report_feedback if f.what_needs_improvement]
        
        summary = FeedbackSummary(
            summary_id=f"summary_{uuid.uuid4().hex[:8]}",
            start_date=start_date,
            end_date=end_date,
            total_feedback=total_feedback,
            avg_rating=avg_rating,
            positive_rate=positive_rate,
            negative_rate=negative_rate,
            improvement_suggestions=improvements[:5],
            rating_trend="stable",  # Simplified
            engagement_trend="stable"  # Added missing field
        )
        
        logger.info(f"Generated feedback summary: {total_feedback} feedbacks, avg={avg_rating:.2f}")
        return summary
    
    def get_low_rated_insights(self, threshold: float = 3.0) -> List[str]:
        """Get insights with low ratings"""
        low_rated = []
        
        for insight_id, feedback_list in self.insight_feedback.items():
            avg_rating = self.get_average_rating(insight_id)
            if avg_rating and avg_rating < threshold:
                low_rated.append(insight_id)
        
        return low_rated
    
    def get_high_engagement_insights(self) -> List[str]:
        """Get insights with high user engagement"""
        engagement_scores = {}
        
        for feedback in self.implicit_feedback:
            insight_id = feedback.insight_id
            
            # Calculate engagement score
            score = 0
            score += feedback.time_spent_viewing / 10  # 10 seconds = 1 point
            if feedback.clicked:
                score += 2
            if feedback.drilled_down:
                score += 3
            if feedback.shared:
                score += 5
            
            if insight_id not in engagement_scores:
                engagement_scores[insight_id] = []
            engagement_scores[insight_id].append(score)
        
        # Average scores
        avg_scores = {
            iid: sum(scores) / len(scores)
            for iid, scores in engagement_scores.items()
        }
        
        # Sort by score
        sorted_insights = sorted(
            avg_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [iid for iid, score in sorted_insights[:10]]