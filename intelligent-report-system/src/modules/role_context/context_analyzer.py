"""
Role-Context Analyzer
Maps roles to data requirements and filters data accordingly
"""
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

from src.modules.role_context.models import (
    RoleProfile, RoleContext, InsightRequirement, DataGranularity
)
from src.modules.role_context.role_repository import RoleRepository
from src.modules.input_processing.models import ProcessedData, StructuredData, TextData
from src.utils.logger import app_logger as logger

class RoleContextAnalyzer:
    """Analyzes and adapts data based on role context"""
    
    def __init__(self):
        self.role_repository = RoleRepository()
        logger.info("RoleContextAnalyzer initialized")
    
    def create_role_context(
        self,
        role_id: str,
        time_period: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        urgency: str = "normal"
    ) -> RoleContext:
        """Create context for a specific role"""
        
        role = self.role_repository.get_role(role_id)
        if not role:
            raise ValueError(f"Role not found: {role_id}")
        
        time_period = time_period or datetime.now().strftime("%Y-Q%q")
        
        context = RoleContext(
            role_profile=role,
            current_time_period=time_period,
            specific_filters=filters or {},
            urgency=urgency
        )
        
        logger.info(f"Created context for role: {role.role_name}")
        return context
    
    def filter_data_for_role(
        self,
        data: ProcessedData,
        role_context: RoleContext
    ) -> ProcessedData:
        """Filter and adapt data based on role requirements"""
        
        role = role_context.role_profile
        logger.info(f"Filtering data for role: {role.role_name}")
        
        # For structured data, apply granularity and department filters
        if isinstance(data, StructuredData):
            return self._filter_structured_data(data, role_context)
        
        # For text data, check relevance to role focus areas
        elif isinstance(data, TextData):
            return self._filter_text_data(data, role_context)
        
        return data
    
    def _filter_structured_data(
        self,
        data: StructuredData,
        role_context: RoleContext
    ) -> StructuredData:
        """Filter structured data based on role"""
        
        role = role_context.role_profile
        access_policy = self.role_repository.get_access_policy(role.role_id)
        
        # Convert to DataFrame for filtering
        df = pd.DataFrame(data.processed_content['data'])
        
        # Apply department filter
        if 'department' in df.columns:
            accessible_depts = [d.value for d in role.accessible_departments]
            df = df[df['department'].isin(accessible_depts)]
        
        # Apply region filter
        if role.accessible_regions and 'region' in df.columns:
            if 'assigned_region' not in role.accessible_regions:
                df = df[df['region'].isin(role.accessible_regions)]
        
        # Apply financial data filter
        if not access_policy.can_view_financial:
            financial_cols = ['salary', 'compensation', 'revenue', 'profit', 'cost']
            cols_to_drop = [col for col in df.columns if any(f in col.lower() for f in financial_cols)]
            df = df.drop(columns=cols_to_drop, errors='ignore')
        
        # Apply data granularity
        df = self._apply_granularity(df, role.data_granularity)
        
        # Update processed content
        data.processed_content['data'] = df.to_dict(orient='records')
        data.processed_content['columns'] = df.columns.tolist()
        
        # Update metadata
        if data.metadata:
            data.metadata.row_count = len(df)
            data.metadata.column_count = len(df.columns)
            data.metadata.columns = df.columns.tolist()
        
        data.processing_steps.append(f"filtered_for_role_{role.role_id}")
        
        logger.info(f"Filtered to {len(df)} rows for {role.role_name}")
        return data
    
    def _apply_granularity(
        self,
        df: pd.DataFrame,
        granularity_levels: List[DataGranularity]
    ) -> pd.DataFrame:
        """Apply data granularity aggregation"""
        
        # If ENTERPRISE level is required, aggregate to highest level
        if DataGranularity.ENTERPRISE in granularity_levels:
            # Aggregate numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                # Simple aggregation (can be made more sophisticated)
                return df
        
        # If TRANSACTION level, return detailed data
        if DataGranularity.TRANSACTION in granularity_levels:
            return df
        
        # Otherwise return as-is (can add more aggregation logic)
        return df
    
    def _filter_text_data(
        self,
        data: TextData,
        role_context: RoleContext
    ) -> TextData:
        """Filter text data based on role relevance"""
        
        role = role_context.role_profile
        text = data.processed_content.lower()
        
        # Check if text is relevant to role's focus areas
        relevance_score = 0
        for focus_area in role.focus_areas:
            if focus_area.replace('_', ' ') in text:
                relevance_score += 1
        
        # Add relevance metadata
        if not data.metadata:
            data.metadata = {}
        
        data.metadata.relevance_score = relevance_score
        data.metadata.relevant_to_role = role.role_name
        
        data.processing_steps.append(f"relevance_scored_for_{role.role_id}")
        
        logger.debug(f"Text relevance score for {role.role_name}: {relevance_score}")
        return data
    
    def get_relevant_kpis(self, role_id: str) -> List[str]:
        """Get KPI names relevant to a role"""
        
        role = self.role_repository.get_role(role_id)
        if not role:
            return []
        
        kpi_names = [kpi.name for kpi in role.primary_kpis]
        kpi_names.extend([kpi.name for kpi in role.secondary_kpis])
        
        return kpi_names
    
    def should_alert(self, role_id: str, alert_type: str) -> bool:
        """Check if role should be alerted for specific event"""
        
        role = self.role_repository.get_role(role_id)
        if not role:
            return False
        
        return alert_type in role.alert_triggers
    
    def get_insight_requirements(self, role_id: str) -> InsightRequirement:
        """Get insight requirements for a role"""
        
        role = self.role_repository.get_role(role_id)
        if not role:
            raise ValueError(f"Role not found: {role_id}")
        
        # Map role level to insight types
        insight_types = []
        
        if role.role_level == "executive":
            insight_types = ["trend", "strategic_risk", "opportunity", "high_level_comparison"]
            max_insights = 5
            min_confidence = 0.8
        elif role.role_level == "director":
            insight_types = ["trend", "comparison", "anomaly", "forecast"]
            max_insights = 8
            min_confidence = 0.75
        elif role.role_level == "manager":
            insight_types = ["anomaly", "trend", "team_performance", "operational_issue"]
            max_insights = 10
            min_confidence = 0.7
        else:  # analyst, specialist
            insight_types = ["detailed_analysis", "root_cause", "variance", "forecast"]
            max_insights = 15
            min_confidence = 0.65
        
        return InsightRequirement(
            role_id=role_id,
            insight_types=insight_types,
            min_confidence=min_confidence,
            max_insights_per_report=max_insights,
            include_explanations=True,
            include_recommendations=role.role_level in ["executive", "director"]
        )
    
    def prioritize_data_sources(
        self,
        data_items: List[ProcessedData],
        role_context: RoleContext
    ) -> List[ProcessedData]:
        """Prioritize data sources based on role relevance"""
        
        role = role_context.role_profile
        scored_items = []
        
        for item in data_items:
            score = 0
            
            # Score based on modality preference
            if item.modality.value == "structured":
                score += 10  # Most roles prefer structured data
            
            # Score based on focus areas (for text)
            if isinstance(item, TextData) and hasattr(item.metadata, 'relevance_score'):
                score += item.metadata.relevance_score * 5
            
            # Score based on department
            if hasattr(item, 'department'):
                if item.department in role.accessible_departments:
                    score += 5
            
            scored_items.append((score, item))
        
        # Sort by score descending
        scored_items.sort(key=lambda x: x[0], reverse=True)
        
        prioritized = [item for score, item in scored_items]
        
        logger.info(f"Prioritized {len(prioritized)} data sources for {role.role_name}")
        return prioritized
    
    def get_recommended_visualizations(self, role_id: str) -> List[str]:
        """Get recommended visualization types for role"""
        
        role = self.role_repository.get_role(role_id)
        if not role:
            return []
        
        return [viz.value for viz in role.preferred_visualizations]
    
    def get_temporal_preference(self, role_id: str) -> List[str]:
        """Get temporal horizons preferred by role"""
        
        role = self.role_repository.get_role(role_id)
        if not role:
            return []
        
        return [horizon.value for horizon in role.temporal_horizons]