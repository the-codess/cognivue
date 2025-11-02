"""
Feedback & Learning Models
Defines feedback structures and learning metrics
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    """Types of feedback"""
    RATING = "rating"
    CORRECTION = "correction"
    ANNOTATION = "annotation"
    FLAG = "flag"
    IMPLICIT = "implicit"

class FeedbackSentiment(str, Enum):
    """Sentiment of feedback"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class InsightFeedback(BaseModel):
    """Feedback on a specific insight"""
    feedback_id: str
    insight_id: str
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    
    # Feedback content
    feedback_type: FeedbackType
    rating: Optional[int] = Field(None, ge=1, le=5)  # 1-5 stars
    is_relevant: Optional[bool] = None
    is_accurate: Optional[bool] = None
    is_actionable: Optional[bool] = None
    
    # User input
    comment: Optional[str] = None
    correction: Optional[str] = None
    tags: List[str] = []
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None

class ReportFeedback(BaseModel):
    """Feedback on entire report"""
    feedback_id: str
    report_id: str
    user_id: Optional[str] = None
    role_id: Optional[str] = None
    
    # Overall ratings
    overall_rating: int = Field(ge=1, le=5)
    relevance_rating: int = Field(ge=1, le=5)
    clarity_rating: int = Field(ge=1, le=5)
    actionability_rating: int = Field(ge=1, le=5)
    
    # Qualitative feedback
    what_worked_well: Optional[str] = None
    what_needs_improvement: Optional[str] = None
    missing_insights: Optional[str] = None
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now)
    time_spent: Optional[float] = None  # seconds

class ImplicitFeedback(BaseModel):
    """Implicit feedback from user behavior"""
    feedback_id: str
    insight_id: str
    user_id: Optional[str] = None
    
    # Interaction metrics
    time_spent_viewing: float  # seconds
    clicked: bool = False
    drilled_down: bool = False
    shared: bool = False
    exported: bool = False
    dismissed: bool = False
    
    # Context
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None

class LearningMetrics(BaseModel):
    """Metrics for system learning"""
    model_config = {"protected_namespaces": ()}  # Allow model_ prefix
    
    metric_id: str
    period_start: datetime
    period_end: datetime
    
    # Insight quality metrics
    avg_insight_rating: float
    avg_relevance_score: float
    avg_accuracy_score: float
    
    # User engagement
    total_feedback_count: int
    positive_feedback_rate: float
    user_satisfaction_score: float
    
    # Learning progress
    model_accuracy: float
    prediction_confidence: float
    improvement_rate: float
    
    # By role
    role_metrics: Dict[str, Dict[str, float]] = {}

class FeedbackSummary(BaseModel):
    """Summary of feedback for a time period"""
    summary_id: str
    start_date: datetime
    end_date: datetime
    
    # Aggregates
    total_feedback: int
    avg_rating: float
    positive_rate: float
    negative_rate: float
    
    # Top issues
    common_complaints: List[str] = []
    improvement_suggestions: List[str] = []
    
    # Trends
    rating_trend: str  # improving, declining, stable
    engagement_trend: str

class AdaptationAction(BaseModel):
    """Action taken by learning system"""
    action_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    # Action details
    action_type: str  # adjust_weights, update_rules, retrain_model
    component: str  # insight_generation, role_filter, etc.
    
    # Changes made
    parameters_changed: Dict[str, Any]
    expected_impact: str
    
    # Validation
    validated: bool = False
    actual_impact: Optional[str] = None