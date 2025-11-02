"""
Statistical Analysis Engine
Performs statistical analysis to detect trends, anomalies, and correlations
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from scipy import stats
from sklearn.ensemble import IsolationForest
import uuid

from src.modules.insight_generation.models import (
    TrendInsight, AnomalyInsight, ComparisonInsight, CorrelationInsight,
    InsightSeverity, DataProvenance, ExplanationComponent
)
from src.utils.logger import app_logger as logger

class StatisticalAnalyzer:
    """Performs statistical analysis on data"""
    
    def __init__(self):
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        logger.info("StatisticalAnalyzer initialized")
    
    def detect_trends(
        self,
        df: pd.DataFrame,
        value_column: str,
        time_column: str = None,
        min_data_points: int = 10
    ) -> List[TrendInsight]:
        """Detect trends in time series data"""
        
        insights = []
        
        try:
            if len(df) < min_data_points:
                logger.warning(f"Insufficient data points for trend analysis: {len(df)}")
                return insights
            
            # Sort by time if time column exists
            if time_column and time_column in df.columns:
                df = df.sort_values(time_column)
            
            # Get values
            values = df[value_column].values
            
            # Calculate trend using linear regression
            x = np.arange(len(values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)
            
            # Determine trend direction and strength
            trend_direction = "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
            trend_strength = abs(r_value)
            
            # Calculate percentage change
            if values[0] != 0:
                percentage_change = ((values[-1] - values[0]) / abs(values[0])) * 100
            else:
                percentage_change = 0
            
            # Determine severity based on change magnitude
            if abs(percentage_change) > 50:
                severity = InsightSeverity.CRITICAL
            elif abs(percentage_change) > 25:
                severity = InsightSeverity.HIGH
            elif abs(percentage_change) > 10:
                severity = InsightSeverity.MEDIUM
            else:
                severity = InsightSeverity.LOW
            
            # Create narrative
            narrative = self._generate_trend_narrative(
                value_column, trend_direction, percentage_change, 
                values[0], values[-1], trend_strength
            )
            
            # Create provenance
            provenance = DataProvenance(
                source_id=f"trend_{uuid.uuid4().hex[:8]}",
                source_type="dataframe",
                source_path=value_column,
                data_points_used=len(values),
                quality_score=min(trend_strength, 1.0)
            )
            
            # Create explanation
            explanation = ExplanationComponent(
                component_type="statistical_analysis",
                content=f"Linear regression analysis shows {trend_direction} trend with R² = {r_value**2:.3f}",
                confidence=min(trend_strength, 1.0),
                supporting_data={
                    "slope": float(slope),
                    "r_squared": float(r_value ** 2),
                    "p_value": float(p_value)
                }
            )
            
            # Create insight
            insight = TrendInsight(
                insight_id=f"trend_{uuid.uuid4().hex[:8]}",
                severity=severity,
                title=f"{trend_direction.title()} Trend in {value_column}",
                description=f"{value_column} shows a {trend_direction} trend",
                narrative=narrative,
                confidence_score=min(trend_strength, 1.0),
                relevance_score=min(abs(percentage_change) / 50, 1.0),
                impact_score=min(abs(percentage_change) / 100, 1.0),
                data_provenance=[provenance],
                explanations=[explanation],
                trend_direction=trend_direction,
                trend_strength=trend_strength,
                time_period="full_period",
                percentage_change=float(percentage_change),
                baseline_value=float(values[0]),
                current_value=float(values[-1]),
                key_metrics={
                    "slope": float(slope),
                    "r_squared": float(r_value ** 2),
                    "data_points": len(values)
                },
                visualizations=["line_chart", "trend_line"],
                tags=["trend", "statistical"]
            )
            
            insights.append(insight)
            logger.info(f"Detected {trend_direction} trend in {value_column}")
            
        except Exception as e:
            logger.error(f"Error detecting trends: {str(e)}")
        
        return insights
    
    def detect_anomalies(
        self,
        df: pd.DataFrame,
        value_column: str,
        threshold: float = 2.0
    ) -> List[AnomalyInsight]:
        """Detect anomalies using statistical methods"""
        
        insights = []
        
        try:
            values = df[value_column].values
            
            if len(values) < 10:
                logger.warning("Insufficient data for anomaly detection")
                return insights
            
            # Calculate z-scores
            mean = np.mean(values)
            std = np.std(values)
            
            if std == 0:
                logger.warning("Zero standard deviation, cannot detect anomalies")
                return insights
            
            z_scores = np.abs((values - mean) / std)
            
            # Find anomalies
            anomaly_indices = np.where(z_scores > threshold)[0]
            
            for idx in anomaly_indices[:5]:  # Limit to top 5 anomalies
                actual_value = values[idx]
                deviation = actual_value - mean
                deviation_type = "positive" if deviation > 0 else "negative"
                
                # Determine severity
                if z_scores[idx] > 4:
                    severity = InsightSeverity.CRITICAL
                elif z_scores[idx] > 3:
                    severity = InsightSeverity.HIGH
                else:
                    severity = InsightSeverity.MEDIUM
                
                # Create narrative
                narrative = self._generate_anomaly_narrative(
                    value_column, actual_value, mean, deviation, z_scores[idx]
                )
                
                # Create provenance
                provenance = DataProvenance(
                    source_id=f"anomaly_{uuid.uuid4().hex[:8]}",
                    source_type="dataframe",
                    source_path=value_column,
                    data_points_used=len(values),
                    quality_score=0.9
                )
                
                # Create explanation
                explanation = ExplanationComponent(
                    component_type="statistical_analysis",
                    content=f"Value deviates {z_scores[idx]:.2f} standard deviations from mean",
                    confidence=min(z_scores[idx] / 4, 1.0),
                    supporting_data={
                        "z_score": float(z_scores[idx]),
                        "mean": float(mean),
                        "std": float(std)
                    }
                )
                
                # Create insight
                insight = AnomalyInsight(
                    insight_id=f"anomaly_{uuid.uuid4().hex[:8]}",
                    severity=severity,
                    title=f"Anomaly Detected in {value_column}",
                    description=f"Unusual value found: {actual_value:.2f}",
                    narrative=narrative,
                    confidence_score=min(z_scores[idx] / 4, 1.0),
                    relevance_score=0.8,
                    impact_score=min(z_scores[idx] / 5, 1.0),
                    data_provenance=[provenance],
                    explanations=[explanation],
                    anomaly_score=float(z_scores[idx] / 5),
                    expected_value=float(mean),
                    actual_value=float(actual_value),
                    deviation=float(deviation),
                    deviation_type=deviation_type,
                    key_metrics={
                        "z_score": float(z_scores[idx]),
                        "standard_deviations": float(z_scores[idx])
                    },
                    visualizations=["scatter_plot", "box_plot"],
                    recommendations=[
                        f"Investigate the cause of this {deviation_type} deviation",
                        "Check for data quality issues or external factors"
                    ],
                    tags=["anomaly", "outlier"]
                )
                
                insights.append(insight)
            
            logger.info(f"Detected {len(insights)} anomalies in {value_column}")
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
        
        return insights
    
    def detect_correlations(
        self,
        df: pd.DataFrame,
        threshold: float = 0.5
    ) -> List[CorrelationInsight]:
        """Detect correlations between numeric columns"""
        
        insights = []
        
        try:
            # Get numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                logger.warning("Insufficient numeric columns for correlation analysis")
                return insights
            
            # Calculate correlation matrix
            corr_matrix = df[numeric_cols].corr()
            
            # Find strong correlations
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    corr_value = corr_matrix.iloc[i, j]
                    
                    if abs(corr_value) >= threshold:
                        col_a = numeric_cols[i]
                        col_b = numeric_cols[j]
                        
                        # Determine relationship type
                        if corr_value > 0:
                            relationship_type = "positive"
                        elif corr_value < 0:
                            relationship_type = "negative"
                        else:
                            relationship_type = "none"
                        
                        # Determine severity
                        if abs(corr_value) > 0.8:
                            severity = InsightSeverity.HIGH
                        elif abs(corr_value) > 0.6:
                            severity = InsightSeverity.MEDIUM
                        else:
                            severity = InsightSeverity.LOW
                        
                        # Create narrative
                        narrative = self._generate_correlation_narrative(
                            col_a, col_b, corr_value, relationship_type
                        )
                        
                        # Create provenance
                        provenance = DataProvenance(
                            source_id=f"corr_{uuid.uuid4().hex[:8]}",
                            source_type="dataframe",
                            source_path=f"{col_a}_vs_{col_b}",
                            data_points_used=len(df),
                            quality_score=0.85
                        )
                        
                        # Create explanation
                        explanation = ExplanationComponent(
                            component_type="statistical_analysis",
                            content=f"Pearson correlation coefficient: {corr_value:.3f}",
                            confidence=abs(corr_value),
                            supporting_data={
                                "correlation": float(corr_value),
                                "sample_size": len(df)
                            }
                        )
                        
                        # Create insight
                        insight = CorrelationInsight(
                            insight_id=f"corr_{uuid.uuid4().hex[:8]}",
                            severity=severity,
                            title=f"{relationship_type.title()} Correlation: {col_a} & {col_b}",
                            description=f"Strong {relationship_type} relationship detected",
                            narrative=narrative,
                            confidence_score=abs(corr_value),
                            relevance_score=abs(corr_value),
                            impact_score=abs(corr_value) * 0.8,
                            data_provenance=[provenance],
                            explanations=[explanation],
                            variable_a=col_a,
                            variable_b=col_b,
                            correlation_coefficient=float(corr_value),
                            relationship_type=relationship_type,
                            statistical_significance=0.95,  # Simplified
                            key_metrics={
                                "correlation": float(corr_value),
                                "sample_size": len(df)
                            },
                            visualizations=["scatter_plot", "correlation_matrix"],
                            tags=["correlation", "relationship"]
                        )
                        
                        insights.append(insight)
            
            logger.info(f"Detected {len(insights)} correlations")
            
        except Exception as e:
            logger.error(f"Error detecting correlations: {str(e)}")
        
        return insights
    
    def compare_groups(
        self,
        df: pd.DataFrame,
        group_column: str,
        value_column: str,
        top_n: int = 3
    ) -> List[ComparisonInsight]:
        """Compare groups within data"""
        
        insights = []
        
        try:
            if group_column not in df.columns or value_column not in df.columns:
                logger.warning(f"Columns not found for comparison")
                return insights
            
            # Group and aggregate
            grouped = df.groupby(group_column)[value_column].agg(['sum', 'mean', 'count'])
            grouped = grouped.sort_values('sum', ascending=False)
            
            # Compare top performers
            for i in range(min(top_n - 1, len(grouped) - 1)):
                entity_a = grouped.index[i]
                entity_b = grouped.index[i + 1]
                
                value_a = grouped.iloc[i]['sum']
                value_b = grouped.iloc[i + 1]['sum']
                
                difference = value_a - value_b
                percentage_diff = (difference / value_b * 100) if value_b != 0 else 0
                
                # Create narrative
                narrative = self._generate_comparison_narrative(
                    entity_a, entity_b, value_column, value_a, value_b, percentage_diff
                )
                
                # Create provenance
                provenance = DataProvenance(
                    source_id=f"comp_{uuid.uuid4().hex[:8]}",
                    source_type="dataframe",
                    source_path=f"{group_column}_{value_column}",
                    data_points_used=len(df),
                    quality_score=0.9
                )
                
                # Create explanation
                explanation = ExplanationComponent(
                    component_type="comparison",
                    content=f"{entity_a} outperforms {entity_b} by {percentage_diff:.1f}%",
                    confidence=0.9,
                    supporting_data={
                        "value_a": float(value_a),
                        "value_b": float(value_b),
                        "difference": float(difference)
                    }
                )
                
                # Determine severity
                if abs(percentage_diff) > 50:
                    severity = InsightSeverity.HIGH
                elif abs(percentage_diff) > 25:
                    severity = InsightSeverity.MEDIUM
                else:
                    severity = InsightSeverity.LOW
                
                # Create insight
                insight = ComparisonInsight(
                    insight_id=f"comp_{uuid.uuid4().hex[:8]}",
                    severity=severity,
                    title=f"{entity_a} vs {entity_b} in {value_column}",
                    description=f"Performance comparison",
                    narrative=narrative,
                    confidence_score=0.9,
                    relevance_score=0.85,
                    impact_score=min(abs(percentage_diff) / 100, 1.0),
                    data_provenance=[provenance],
                    explanations=[explanation],
                    entity_a=str(entity_a),
                    entity_b=str(entity_b),
                    metric=value_column,
                    value_a=float(value_a),
                    value_b=float(value_b),
                    difference=float(difference),
                    percentage_difference=float(percentage_diff),
                    key_metrics={
                        "difference": float(difference),
                        "percentage": float(percentage_diff)
                    },
                    visualizations=["bar_chart", "comparison_table"],
                    tags=["comparison", "performance"]
                )
                
                insights.append(insight)
            
            logger.info(f"Generated {len(insights)} comparisons")
            
        except Exception as e:
            logger.error(f"Error in group comparison: {str(e)}")
        
        return insights
    
    def _generate_trend_narrative(
        self, column: str, direction: str, pct_change: float,
        start_val: float, end_val: float, strength: float
    ) -> str:
        """Generate natural language narrative for trend"""
        
        strength_word = "strongly" if strength > 0.7 else "moderately" if strength > 0.4 else "slightly"
        
        narrative = f"{column} has {strength_word} {direction} "
        narrative += f"by {abs(pct_change):.1f}% "
        narrative += f"from {start_val:.2f} to {end_val:.2f}. "
        
        if abs(pct_change) > 25:
            narrative += "This represents a significant change that warrants attention."
        elif abs(pct_change) > 10:
            narrative += "This is a notable change in the metric."
        else:
            narrative += "This is a modest change."
        
        return narrative
    
    def _generate_anomaly_narrative(
        self, column: str, actual: float, expected: float, 
        deviation: float, z_score: float
    ) -> str:
        """Generate natural language narrative for anomaly"""
        
        direction = "higher" if deviation > 0 else "lower"
        
        narrative = f"An unusual value of {actual:.2f} was detected in {column}, "
        narrative += f"which is {abs(deviation):.2f} {direction} than the expected value of {expected:.2f}. "
        narrative += f"This represents a deviation of {z_score:.1f} standard deviations. "
        
        if z_score > 4:
            narrative += "This is an extreme outlier that requires immediate investigation."
        elif z_score > 3:
            narrative += "This is a significant anomaly that should be reviewed."
        else:
            narrative += "This warrants further examination."
        
        return narrative
    
    def _generate_correlation_narrative(
        self, var_a: str, var_b: str, corr: float, rel_type: str
    ) -> str:
        """Generate natural language narrative for correlation"""
        
        strength = "strong" if abs(corr) > 0.7 else "moderate" if abs(corr) > 0.5 else "weak"
        
        narrative = f"A {strength} {rel_type} correlation (r={corr:.3f}) exists between {var_a} and {var_b}. "
        
        if rel_type == "positive":
            narrative += f"As {var_a} increases, {var_b} tends to increase as well."
        elif rel_type == "negative":
            narrative += f"As {var_a} increases, {var_b} tends to decrease."
        
        return narrative
    
    def _generate_comparison_narrative(
        self, entity_a: str, entity_b: str, metric: str,
        value_a: float, value_b: float, pct_diff: float
    ) -> str:
        """Generate natural language narrative for comparison"""
        
        if value_a > value_b:
            leader = entity_a
            follower = entity_b
        else:
            leader = entity_b
            follower = entity_a
            pct_diff = abs(pct_diff)
        
        narrative = f"{leader} leads {follower} in {metric} by {pct_diff:.1f}%. "
        narrative += f"{leader} achieved {value_a:.2f} compared to {follower}'s {value_b:.2f}. "
        
        if pct_diff > 50:
            narrative += "This represents a substantial performance gap."
        elif pct_diff > 25:
            narrative += "This is a significant difference in performance."
        else:
            narrative += "The performance gap is relatively modest."
        
        return narrative