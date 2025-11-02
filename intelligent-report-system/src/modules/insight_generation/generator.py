"""
Insight Generator
Main orchestrator for generating insights from processed data
"""
import pandas as pd
from typing import List, Optional
import uuid
from datetime import datetime

from src.modules.insight_generation.models import (
    Insight, InsightCollection, InsightGenerationConfig, InsightSeverity
)
from src.modules.insight_generation.statistical_analyzer import StatisticalAnalyzer
from src.modules.input_processing.models import ProcessedData, StructuredData
from src.modules.role_context.models import RoleContext, InsightRequirement
from src.utils.logger import app_logger as logger

class InsightGenerator:
    """Generate actionable insights from data"""
    
    def __init__(self, config: Optional[InsightGenerationConfig] = None):
        self.config = config or InsightGenerationConfig()
        self.statistical_analyzer = StatisticalAnalyzer()
        logger.info("InsightGenerator initialized")
    
    def generate_insights(
        self,
        data: ProcessedData,
        role_context: Optional[RoleContext] = None,
        insight_requirement: Optional[InsightRequirement] = None
    ) -> InsightCollection:
        """Generate insights from processed data"""
        
        logger.info(f"Generating insights for {data.modality.value} data")
        
        all_insights = []
        
        # Only process structured data for now
        if isinstance(data, StructuredData):
            all_insights.extend(self._generate_from_structured(data))
        
        # Apply role-based filtering if context provided
        if role_context and insight_requirement:
            all_insights = self._filter_for_role(all_insights, insight_requirement)
        
        # Sort by relevance and impact
        all_insights = self._prioritize_insights(all_insights)
        
        # Limit to max insights
        max_insights = insight_requirement.max_insights_per_report if insight_requirement else self.config.max_insights
        all_insights = all_insights[:max_insights]
        
        # Create collection
        collection = self._create_collection(
            all_insights,
            role_context.role_profile.role_id if role_context else "general"
        )
        
        logger.info(f"Generated {len(all_insights)} insights")
        return collection
    
    def _generate_from_structured(self, data: StructuredData) -> List[Insight]:
        """Generate insights from structured data"""
        
        insights = []
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data.processed_content['data'])
            
            if len(df) == 0:
                logger.warning("Empty dataframe, no insights generated")
                return insights
            
            # Get numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) == 0:
                logger.warning("No numeric columns for analysis")
                return insights
            
            # Detect trends
            if self.config.detect_trends and len(numeric_cols) > 0:
                for col in numeric_cols[:3]:  # Analyze top 3 numeric columns
                    try:
                        trend_insights = self.statistical_analyzer.detect_trends(
                            df, col, min_data_points=self.config.trend_min_data_points
                        )
                        insights.extend(trend_insights)
                    except Exception as e:
                        logger.error(f"Error detecting trends in {col}: {str(e)}")
            
            # Detect anomalies
            if self.config.detect_anomalies and len(numeric_cols) > 0:
                for col in numeric_cols[:2]:  # Analyze top 2 columns
                    try:
                        anomaly_insights = self.statistical_analyzer.detect_anomalies(
                            df, col, threshold=self.config.anomaly_threshold
                        )
                        insights.extend(anomaly_insights)
                    except Exception as e:
                        logger.error(f"Error detecting anomalies in {col}: {str(e)}")
            
            # Detect correlations
            if self.config.detect_correlations and len(numeric_cols) >= 2:
                try:
                    corr_insights = self.statistical_analyzer.detect_correlations(
                        df, threshold=self.config.correlation_threshold
                    )
                    insights.extend(corr_insights)
                except Exception as e:
                    logger.error(f"Error detecting correlations: {str(e)}")
            
            # Compare groups if categorical columns exist
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                try:
                    comp_insights = self.statistical_analyzer.compare_groups(
                        df, categorical_cols[0], numeric_cols[0]
                    )
                    insights.extend(comp_insights)
                except Exception as e:
                    logger.error(f"Error comparing groups: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error generating insights from structured data: {str(e)}")
        
        return insights
    
    # def _filter_for_role(
    #     self,
    #     insights: List[Insight],
    #     requirement: InsightRequirement
    # ) -> List[Insight]:
    #     """Filter insights based on role requirements"""
        
    #     filtered = []
        
    #     for insight in insights:
    #         # Check confidence threshold
    #         if insight.confidence_score < requirement.min_confidence:
    #             continue
            
    #         # Check insight type
    #         if insight.insight_type.value not in requirement.insight_types:
    #             continue
            
    #         # Add role context
    #         insight.for_role = requirement.role_id
            
    #         filtered.append(insight)
        
    #     logger.info(f"Filtered to {len(filtered)} insights for role")
    #     return filtered
    def _filter_for_role(
        self,
        insights: List[Insight],
        requirement: InsightRequirement
    ) -> List[Insight]:
        """Filter insights based on role requirements with more lenient matching"""
        
        filtered = []
        
        # Log the filtering process for debugging
        logger.info(f"Starting filter with {len(insights)} insights for role {requirement.role_id}")
        logger.info(f"Role requirements - min_confidence: {requirement.min_confidence}, types: {requirement.insight_types}")
        
        for insight in insights:
            # Check confidence threshold - be slightly more lenient
            min_threshold = max(0.5, requirement.min_confidence - 0.1)  # Allow 10% below threshold
            if insight.confidence_score < min_threshold:
                logger.debug(f"Filtered out '{insight.title}' - confidence {insight.confidence_score:.2f} below {min_threshold:.2f}")
                continue
            
            # Check insight type - be very lenient with matching
            insight_type = insight.insight_type.value.lower()
            
            # Default to accepting the insight
            type_matches = False
            
            # Map common insight types
            type_mapping = {
                'trend': ['trend', 'trending', 'pattern', 'movement'],
                'anomaly': ['anomaly', 'outlier', 'unusual', 'spike', 'drop'],
                'comparison': ['comparison', 'compare', 'difference', 'versus', 'vs'],
                'correlation': ['correlation', 'relationship', 'association', 'related'],
                'summary': ['summary', 'overview', 'aggregate', 'total'],
                'forecast': ['forecast', 'prediction', 'projection', 'future']
            }
            
            # Check against requirement types
            for req_type in requirement.insight_types:
                req_type_lower = req_type.lower()
                
                # Direct match
                if req_type_lower in insight_type or insight_type in req_type_lower:
                    type_matches = True
                    break
                
                # Check mapped terms
                for base_type, synonyms in type_mapping.items():
                    if any(syn in req_type_lower for syn in synonyms):
                        if any(syn in insight_type for syn in synonyms):
                            type_matches = True
                            break
                
                if type_matches:
                    break
                
                # Word-level matching
                req_words = set(req_type_lower.split('_'))
                insight_words = set(insight_type.split('_'))
                if req_words & insight_words:  # Any common word
                    type_matches = True
                    break
            
            # Role-specific overrides - accept common insight types
            if not type_matches:
                if requirement.role_id in ['regional_sales_manager', 'financial_analyst', 'operations_manager']:
                    # Managers and analysts want most insight types
                    if insight_type in ['trend', 'anomaly', 'comparison', 'correlation', 'summary']:
                        type_matches = True
                        logger.debug(f"Accepted '{insight.title}' via manager role override")
                
                elif requirement.role_id in ['cfo', 'marketing_director', 'ceo']:
                    # Executives want high-level insights
                    if insight_type in ['trend', 'comparison', 'summary', 'forecast']:
                        type_matches = True
                        logger.debug(f"Accepted '{insight.title}' via executive role override")
            
            # If still no match, accept anyway if confidence is very high
            if not type_matches and insight.confidence_score >= 0.85:
                type_matches = True
                logger.debug(f"Accepted '{insight.title}' due to high confidence ({insight.confidence_score:.2f})")
            
            if not type_matches:
                logger.debug(f"Filtered out '{insight.title}' - type '{insight_type}' doesn't match requirements")
                continue
            
            # Add role context
            insight.for_role = requirement.role_id
            filtered.append(insight)
            logger.debug(f"Accepted insight: '{insight.title}' (type: {insight_type}, confidence: {insight.confidence_score:.2f})")
        
        logger.info(f"Filtered to {len(filtered)} insights for role (from {len(insights)} total)")
        
        # If we filtered everything out, return the top insights anyway
        if len(filtered) == 0 and len(insights) > 0:
            logger.warning("All insights filtered out - returning top 3 by confidence")
            sorted_insights = sorted(insights, key=lambda x: x.confidence_score, reverse=True)
            for insight in sorted_insights[:3]:
                insight.for_role = requirement.role_id
                filtered.append(insight)
        
        return filtered
    
    def _prioritize_insights(self, insights: List[Insight]) -> List[Insight]:
        """Prioritize insights by relevance and impact"""
        
        # Calculate priority score
        for insight in insights:
            priority_score = (
                insight.relevance_score * 0.4 +
                insight.impact_score * 0.3 +
                insight.confidence_score * 0.3
            )
            
            # Boost critical insights
            if insight.severity == InsightSeverity.CRITICAL:
                priority_score *= 1.5
            elif insight.severity == InsightSeverity.HIGH:
                priority_score *= 1.2
            
            insight.key_metrics['priority_score'] = priority_score
        
        # Sort by priority
        insights.sort(
            key=lambda x: x.key_metrics.get('priority_score', 0),
            reverse=True
        )
        
        return insights
    
    def _create_collection(
        self,
        insights: List[Insight],
        role_id: str
    ) -> InsightCollection:
        """Create insight collection"""
        
        # Calculate aggregates
        if len(insights) > 0:
            avg_confidence = sum(i.confidence_score for i in insights) / len(insights)
            avg_relevance = sum(i.relevance_score for i in insights) / len(insights)
        else:
            avg_confidence = 0
            avg_relevance = 0
        
        # Count by severity
        critical_count = sum(1 for i in insights if i.severity == InsightSeverity.CRITICAL)
        high_count = sum(1 for i in insights if i.severity == InsightSeverity.HIGH)
        
        # Get unique data sources
        data_sources = list(set(
            prov.source_path
            for insight in insights
            for prov in insight.data_provenance
        ))
        
        collection = InsightCollection(
            collection_id=f"coll_{uuid.uuid4().hex[:8]}",
            for_role=role_id,
            time_period=datetime.now().strftime("%Y-Q%m"),
            insights=insights,
            total_count=len(insights),
            avg_confidence=avg_confidence,
            avg_relevance=avg_relevance,
            critical_insights=critical_count,
            high_priority_insights=high_count,
            data_sources=data_sources
        )
        
        return collection
    
    def generate_summary(self, collection: InsightCollection) -> str:
        """Generate executive summary of insights"""
        
        if collection.total_count == 0:
            return "No significant insights were generated from the available data."
        
        summary = f"Analysis Summary for {collection.for_role}:\n\n"
        
        # Overview
        summary += f"Generated {collection.total_count} insights with "
        summary += f"average confidence of {collection.avg_confidence:.1%}.\n\n"
        
        # Critical insights
        if collection.critical_insights > 0:
            summary += f"🔴 {collection.critical_insights} CRITICAL insights require immediate attention:\n"
            for insight in collection.insights:
                if insight.severity == InsightSeverity.CRITICAL:
                    summary += f"  • {insight.title}\n"
            summary += "\n"
        
        # High priority
        if collection.high_priority_insights > 0:
            summary += f"🟠 {collection.high_priority_insights} HIGH priority insights:\n"
            for insight in collection.insights:
                if insight.severity == InsightSeverity.HIGH:
                    summary += f"  • {insight.title}\n"
            summary += "\n"
        
        # Top 3 insights
        summary += "Top Insights:\n"
        for i, insight in enumerate(collection.insights[:3], 1):
            summary += f"{i}. {insight.title}\n"
            summary += f"   {insight.description}\n"
        
        return summary