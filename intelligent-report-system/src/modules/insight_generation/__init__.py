"""
Insight Generation Module
Generates actionable insights with explanations
"""
from src.modules.insight_generation.models import (
    Insight,
    InsightType,
    InsightSeverity,
    TrendInsight,
    AnomalyInsight,
    ComparisonInsight,
    CorrelationInsight,
    InsightCollection,
    InsightGenerationConfig,
    DataProvenance,
    ExplanationComponent
)
from src.modules.insight_generation.statistical_analyzer import StatisticalAnalyzer
from src.modules.insight_generation.generator import InsightGenerator

__all__ = [
    'Insight',
    'InsightType',
    'InsightSeverity',
    'TrendInsight',
    'AnomalyInsight',
    'ComparisonInsight',
    'CorrelationInsight',
    'InsightCollection',
    'InsightGenerationConfig',
    'DataProvenance',
    'ExplanationComponent',
    'StatisticalAnalyzer',
    'InsightGenerator'
]