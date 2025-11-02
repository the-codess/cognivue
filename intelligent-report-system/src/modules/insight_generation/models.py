"""
Insight Generation Models
Defines insight types and explanation structures
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class InsightType(str, Enum):
    """Types of insights"""
    TREND = "trend"
    ANOMALY = "anomaly"
    COMPARISON = "comparison"
    CORRELATION = "correlation"
    FORECAST = "forecast"
    PATTERN = "pattern"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    RECOMMENDATION = "recommendation"

class InsightSeverity(str, Enum):
    """Severity/importance level"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class DataProvenance(BaseModel):
    """Track data sources for insights"""
    source_id: str
    source_type: str
    source_path: str
    data_points_used: int
    time_range: Optional[str] = None
    quality_score: float = Field(ge=0.0, le=1.0, default=1.0)

class ExplanationComponent(BaseModel):
    """Individual explanation element"""
    component_type: str  # feature_attribution, rule, counterfactual, narrative
    content: str
    supporting_data: Optional[Dict[str, Any]] = None
    confidence: float = Field(ge=0.0, le=1.0)

class Insight(BaseModel):
    """Generated insight with explanation"""
    insight_id: str
    insight_type: InsightType
    severity: InsightSeverity
    
    # Core content
    title: str
    description: str
    narrative: str  # Natural language explanation
    
    # Quantitative measures
    confidence_score: float = Field(ge=0.0, le=1.0)
    relevance_score: float = Field(ge=0.0, le=1.0)
    impact_score: float = Field(ge=0.0, le=1.0)
    
    # Explanation components
    data_provenance: List[DataProvenance]
    explanations: List[ExplanationComponent]
    
    # Supporting evidence
    key_metrics: Dict[str, Any] = {}
    visualizations: List[str] = []  # Recommended viz types
    
    # Recommendations
    recommendations: List[str] = []
    next_steps: List[str] = []
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.now)
    for_role: Optional[str] = None
    tags: List[str] = []

class TrendInsight(Insight):
    """Trend-specific insight"""
    insight_type: InsightType = InsightType.TREND
    trend_direction: str  # increasing, decreasing, stable, volatile
    trend_strength: float = Field(ge=0.0, le=1.0)
    time_period: str
    percentage_change: Optional[float] = None
    baseline_value: Optional[float] = None
    current_value: Optional[float] = None

class AnomalyInsight(Insight):
    """Anomaly detection insight"""
    insight_type: InsightType = InsightType.ANOMALY
    anomaly_score: float = Field(ge=0.0, le=1.0)
    expected_value: float
    actual_value: float
    deviation: float
    deviation_type: str  # positive, negative
    historical_context: Optional[str] = None

class ComparisonInsight(Insight):
    """Comparison insight"""
    insight_type: InsightType = InsightType.COMPARISON
    entity_a: str
    entity_b: str
    metric: str
    value_a: float
    value_b: float
    difference: float
    percentage_difference: float

class CorrelationInsight(Insight):
    """Correlation insight"""
    insight_type: InsightType = InsightType.CORRELATION
    variable_a: str
    variable_b: str
    correlation_coefficient: float = Field(ge=-1.0, le=1.0)
    relationship_type: str  # positive, negative, none
    statistical_significance: float

class InsightCollection(BaseModel):
    """Collection of insights for a report"""
    collection_id: str
    generated_at: datetime = Field(default_factory=datetime.now)
    for_role: str
    time_period: str
    
    insights: List[Insight]
    total_count: int
    
    # Aggregated scores
    avg_confidence: float
    avg_relevance: float
    
    # Summary
    critical_insights: int
    high_priority_insights: int
    
    # Metadata
    data_sources: List[str]
    processing_time: Optional[float] = None

class InsightGenerationConfig(BaseModel):
    """Configuration for insight generation"""
    min_confidence: float = Field(ge=0.0, le=1.0, default=0.7)
    max_insights: int = Field(default=10, ge=1)
    
    # Feature flags
    detect_trends: bool = True
    detect_anomalies: bool = True
    detect_correlations: bool = True
    generate_forecasts: bool = False
    
    # Thresholds
    anomaly_threshold: float = Field(default=2.0, ge=1.0)
    correlation_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    trend_min_data_points: int = Field(default=10, ge=3)
    
    # Explanation depth
    include_explanations: bool = True
    include_recommendations: bool = True
    explanation_detail_level: str = "medium"  # low, medium, high