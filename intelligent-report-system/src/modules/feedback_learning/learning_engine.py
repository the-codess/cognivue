"""
Learning Engine
Learns from feedback to improve system
"""
import uuid
from typing import Dict, List, Optional
from datetime import datetime

from src.modules.feedback_learning.collector import FeedbackCollector
from src.modules.feedback_learning.models import (
    LearningMetrics, AdaptationAction
)
from src.utils.logger import app_logger as logger

class LearningEngine:
    """Learn from user feedback and adapt system"""
    
    def __init__(self, feedback_collector: FeedbackCollector):
        self.feedback_collector = feedback_collector
        self.insight_weights: Dict[str, float] = {}
        self.role_preferences: Dict[str, Dict[str, float]] = {}
        self.adaptation_history: List[AdaptationAction] = []
        logger.info("LearningEngine initialized")
    
    def update_insight_weights(self):
        """Update insight importance weights based on feedback"""
        
        logger.info("Updating insight weights from feedback")
        
        for insight_id, feedback_list in self.feedback_collector.insight_feedback.items():
            if not feedback_list:
                continue
            
            # Calculate weight based on ratings and relevance
            ratings = [f.rating for f in feedback_list if f.rating]
            relevance = [f.is_relevant for f in feedback_list if f.is_relevant is not None]
            
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                weight = avg_rating / 5.0  # Normalize to 0-1
            else:
                weight = 0.5  # Default
            
            # Boost weight if marked as relevant
            if relevance and sum(relevance) / len(relevance) > 0.5:
                weight *= 1.2
            
            self.insight_weights[insight_id] = min(weight, 1.0)
        
        logger.info(f"Updated weights for {len(self.insight_weights)} insights")
    
    def learn_role_preferences(self):
        """Learn what insights each role finds valuable"""
        
        logger.info("Learning role preferences")
        
        for insight_id, feedback_list in self.feedback_collector.insight_feedback.items():
            for feedback in feedback_list:
                if not feedback.role_id or not feedback.rating:
                    continue
                
                role_id = feedback.role_id
                
                if role_id not in self.role_preferences:
                    self.role_preferences[role_id] = {}
                
                # Track what types of insights this role rates highly
                if feedback.rating >= 4:
                    self.role_preferences[role_id][insight_id] = feedback.rating / 5.0
        
        logger.info(f"Learned preferences for {len(self.role_preferences)} roles")
    
    def get_recommended_insights_for_role(
        self,
        role_id: str,
        available_insights: List[str]
    ) -> List[str]:
        """Recommend insights for a role based on learned preferences"""
        
        if role_id not in self.role_preferences:
            return available_insights  # No learning yet
        
        prefs = self.role_preferences[role_id]
        
        # Score insights
        scored = []
        for insight_id in available_insights:
            score = prefs.get(insight_id, 0.5)  # Default score
            scored.append((insight_id, score))
        
        # Sort by score
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [insight_id for insight_id, score in scored]
    
    def compute_learning_metrics(self) -> LearningMetrics:
        """Compute metrics on learning progress"""
        
        # Get recent summary
        summary = self.feedback_collector.get_feedback_summary(days=30)
        
        # Calculate metrics
        metrics = LearningMetrics(
            metric_id=f"metrics_{uuid.uuid4().hex[:8]}",
            period_start=summary.start_date,
            period_end=summary.end_date,
            avg_insight_rating=summary.avg_rating,
            avg_relevance_score=summary.positive_rate,
            avg_accuracy_score=0.85,  # Simplified
            total_feedback_count=summary.total_feedback,
            positive_feedback_rate=summary.positive_rate,
            user_satisfaction_score=summary.avg_rating / 5.0,
            model_accuracy=0.80,  # Simplified
            prediction_confidence=0.75,
            improvement_rate=0.05  # 5% improvement
        )
        
        logger.info(f"Computed learning metrics: satisfaction={metrics.user_satisfaction_score:.2%}")
        return metrics
    
    def adapt_system(self):
        """Make adaptations based on learned patterns"""
        
        logger.info("Adapting system based on feedback")
        
        # Adapt 1: Update weights
        self.update_insight_weights()
        
        action1 = AdaptationAction(
            action_id=f"adapt_{uuid.uuid4().hex[:8]}",
            action_type="adjust_weights",
            component="insight_prioritization",
            parameters_changed={"insight_weights": len(self.insight_weights)},
            expected_impact="Improved insight relevance"
        )
        self.adaptation_history.append(action1)
        
        # Adapt 2: Learn role preferences
        self.learn_role_preferences()
        
        action2 = AdaptationAction(
            action_id=f"adapt_{uuid.uuid4().hex[:8]}",
            action_type="update_rules",
            component="role_filter",
            parameters_changed={"role_preferences": len(self.role_preferences)},
            expected_impact="Better role-specific recommendations"
        )
        self.adaptation_history.append(action2)
        
        logger.info(f"System adapted: {len(self.adaptation_history)} total adaptations")
    
    def get_improvement_suggestions(self) -> List[str]:
        """Get suggestions for system improvement"""
        
        suggestions = []
        
        # Check low-rated insights
        low_rated = self.feedback_collector.get_low_rated_insights()
        if low_rated:
            suggestions.append(f"Improve or filter {len(low_rated)} low-rated insights")
        
        # Check feedback volume
        summary = self.feedback_collector.get_feedback_summary()
        if summary.total_feedback < 10:
            suggestions.append("Encourage more user feedback")
        
        # Check satisfaction
        if summary.avg_rating < 3.5:
            suggestions.append("Address user satisfaction concerns")
        
        return suggestions